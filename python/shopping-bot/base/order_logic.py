import time
import requests
from mistralai import Mistral
import json
import logging
import os
import redis
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("food_order_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Redis client setup
try:
    redis_client = redis.Redis(host='localhost', port=8105, db=0, decode_responses=True)
    redis_client.ping()  # Test connection
    logger.info("Connected to Redis successfully")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {str(e)}")
    raise

# Mistral API key from environment variable
try:
    MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=MISTRAL_API_KEY)
    logger.info("Mistral API client initialized successfully")
except KeyError as e:
    logger.error("MISTRAL_API_KEY environment variable not set")
    raise EnvironmentError("MISTRAL_API_KEY environment variable is required") from e
except Exception as e:
    logger.error(f"Failed to initialize Mistral client: {str(e)}")
    raise

# API endpoints
MENU_API_URL = "https://gaganyatri-mock-restaurant-api.hf.space/menu"
USERS_API_URL = "https://gaganyatri-mock-restaurant-api.hf.space/users/{}"  # Update to production endpoint later

# Tool call to fetch all restaurants and their menus from API with retry
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=lambda retry_state: logger.info(f"Retrying fetch_menu_from_api: attempt {retry_state.attempt_number}")
)
def fetch_menu_from_api():
    logger.info(f"Fetching menu from API: {MENU_API_URL}")
    try:
        response = requests.get(MENU_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.info("Successfully fetched menu")
        return None, data.get("restaurants", {})
    except requests.RequestException as e:
        logger.error(f"Failed to fetch menu from API: {str(e)}")
        raise

# Tool call to fetch user credentials from API with retry
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=lambda retry_state: logger.info(f"Retrying fetch_user_credentials_from_api: attempt {retry_state.attempt_number}")
)
def fetch_user_credentials_from_api(user_id="user1"):
    logger.info(f"Fetching user credentials for user_id: {user_id}")
    try:
        url = USERS_API_URL.format(user_id)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        logger.info(f"Successfully fetched user credentials for {user_id}")
        return None, response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch user credentials: {str(e)}")
        raise

# Function to search menu and parse order using Mistral API with retry
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(Exception),
    before_sleep=lambda retry_state: logger.info(f"Retrying parse_and_search_order: attempt {retry_state.attempt_number}")
)
def parse_and_search_order(user_input, restaurants):
    logger.info(f"Parsing order input: {user_input}")
    try:
        all_items = []
        for rest_id, rest_data in restaurants.items():
            for item_id, item in rest_data["menu"].items():
                all_items.append(f"{item['name']} (from {rest_data['name']})")
        menu_str = ", ".join(all_items)
        
        prompt = f"""
        You are a food order bot. The menu items available across multiple restaurants are: {menu_str}.
        Parse the user's input into a structured order (item names and quantities).
        The user may request multiple items in a single query.
        User input: "{user_input}"
        Respond in JSON format: 
        - For valid orders: [{{"item": "item_name", "quantity": number}}, ...]
        - For invalid orders: {{"error": "message"}}
        Match item names exactly as they appear in the menu (case-insensitive).
        If no quantity is specified, assume 1.
        """
        
        model = "mistral-large-latest"
        messages = [
            {
                "role": "system",
                "content": "Please provide a concise answer in English. Output the response in the requested format. Do not explain the output. Do not add anything new"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        
        chat_response = client.chat.complete(model=model, messages=messages)
        result = json.loads(chat_response.choices[0].message.content)
        
        if "error" in result:
            logger.warning(f"Invalid order input: {result['error']}")
            return result["error"], {}
        
        order = {}
        feedback = []
        for order_item in result:
            item_name = order_item["item"]
            qty = order_item["quantity"]
            
            found = False
            for rest_id, rest_data in restaurants.items():
                for item_id, item in rest_data["menu"].items():
                    if item["name"].lower() == item_name.lower():
                        order_key = f"{rest_id}:{item_id}"
                        order[order_key] = qty
                        feedback.append(f"Added {qty} x {item['name']} (from {rest_data['name']}) to your order.")
                        found = True
                        break
                if found:
                    break
            if not found:
                feedback.append(f"Sorry, '{item_name}' is not available at any restaurant.")
        
        logger.info(f"Order parsed successfully: {order}")
        return "\n".join(feedback), order
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Mistral API response: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error processing order with Mistral API: {str(e)}")
        raise

# Function to check if all items are from a single restaurant
def is_single_restaurant(order):
    if not order:
        return True
    restaurant_ids = {order_key.split(":")[0] for order_key in order.keys()}
    return len(restaurant_ids) == 1

# Function to generate order summary
def generate_order_summary(order, restaurants):
    if not order:
        return "No items in your order."
    
    summary = ["=== Current Order ==="]
    total = 0
    for order_key, qty in order.items():
        rest_id, item_id = order_key.split(":")
        item = restaurants[rest_id]["menu"][item_id]
        rest_name = restaurants[rest_id]["name"]
        cost = item["price"] * qty
        total += cost
        summary.append(f"{item['name']} x{qty} (from {rest_name}) - ₹{cost}")
    summary.append(f"Total: ₹{total}")
    return "\n".join(summary)

# Function to remove an item from the order
def remove_item_from_order(item_name, order, restaurants):
    logger.info(f"Attempting to remove item: {item_name}")
    item_name = item_name.lower()
    for order_key, qty in list(order.items()):
        rest_id, item_id = order_key.split(":")
        item = restaurants[rest_id]["menu"][item_id]
        if item["name"].lower() == item_name:
            del order[order_key]
            logger.info(f"Removed {item['name']} from order")
            return f"Removed {item['name']} from your order."
    logger.warning(f"Item not found in order: {item_name}")
    return f"'{item_name}' not found in your order."

# Functions to manage state in Redis
def save_state(session_id, order, restaurants, awaiting_confirmation):
    try:
        state = {
            "order": order,
            "restaurants": restaurants,
            "awaiting_confirmation": awaiting_confirmation
        }
        redis_client.setex(session_id, 3600, json.dumps(state))  # Expire in 1 hour
        logger.info(f"Saved state for session {session_id}")
    except redis.RedisError as e:
        logger.error(f"Failed to save state to Redis: {str(e)}")

def load_state(session_id):
    try:
        state_json = redis_client.get(session_id)
        if state_json:
            state = json.loads(state_json)
            return state["order"], state["restaurants"], state["awaiting_confirmation"]
        logger.info(f"No state found for session {session_id}, initializing new state")
        return {}, {}, False
    except redis.RedisError as e:
        logger.error(f"Failed to load state from Redis: {str(e)}")
        return {}, {}, False

# Core order processing logic with Redis state
def process_order(session_id, user_input):
    logger.info(f"Processing user input for session {session_id}: {user_input}")
    order, restaurants, awaiting_confirmation = load_state(session_id)
    
    if not restaurants:
        error, loaded_restaurants = fetch_menu_from_api()
        if error:
            return error
        restaurants = loaded_restaurants
        save_state(session_id, order, restaurants, awaiting_confirmation)
    
    user_input = user_input.strip().lower()
    
    try:
        # Handle confirmation for multi-restaurant orders
        if awaiting_confirmation:
            if user_input in ["yes", "y"]:
                error, credentials = fetch_user_credentials_from_api()
                if error:
                    logger.error(f"Cannot proceed due to: {error}")
                    return error
                
                name = credentials.get("name", "Unknown")
                address = credentials.get("address", "Unknown Address")
                phone = credentials.get("phone", "Unknown Phone")
                summary = generate_order_summary(order, restaurants)
                delivery_info = f"Delivery to: {name}, {address}, {phone}"
                logger.info("Order confirmed and processed successfully")
                response = f"{summary}\n{delivery_info}\n\nProcessing your order...\nOrder placed successfully! You'll receive a confirmation soon."
                save_state(session_id, {}, restaurants, False)
                return response
            elif user_input in ["no", "n"]:
                logger.info("Order cancelled by user")
                response = "Order cancelled. Please order from a single restaurant. What would you like to order next?"
                save_state(session_id, {}, restaurants, False)
                return response
            else:
                logger.warning(f"Invalid confirmation response: {user_input}")
                return "Please respond with 'yes' or 'no' to confirm the order."
        
        # Handle "done" command
        if user_input == "done":
            if not order:
                logger.info("No items in order when 'done' received")
                return "No order to process. What would you like to order?"
            
            summary = generate_order_summary(order, restaurants)
            if is_single_restaurant(order):
                error, credentials = fetch_user_credentials_from_api()
                if error:
                    logger.error(f"Cannot proceed due to: {error}")
                    return error
                
                name = credentials.get("name", "Unknown")
                address = credentials.get("address", "Unknown Address")
                phone = credentials.get("phone", "Unknown Phone")
                delivery_info = f"Delivery to: {name}, {address}, {phone}"
                logger.info("Order processed successfully from single restaurant")
                response = f"{summary}\n{delivery_info}\n\nProcessing your order...\nOrder placed successfully! You'll receive a confirmation soon."
                save_state(session_id, {}, restaurants, False)
                return response
            else:
                logger.info("Order contains items from multiple restaurants")
                save_state(session_id, order, restaurants, True)
                return f"{summary}\n\nYour order contains items from multiple restaurants. Typically, orders are from a single restaurant. Confirm order? (yes/no)"
        
        # Handle "show order" command
        if user_input == "show order":
            summary = generate_order_summary(order, restaurants)
            logger.info("Showing current order")
            return f"{summary}\n\nWhat else would you like to order? (Type 'done' to finish)"
        
        # Handle "remove [item]" command
        if user_input.startswith("remove "):
            item_name = user_input.replace("remove ", "").strip()
            if not item_name:
                logger.warning("No item specified for removal")
                return "Please specify an item to remove (e.g., 'remove butter chicken')."
            feedback = remove_item_from_order(item_name, order, restaurants)
            save_state(session_id, order, restaurants, awaiting_confirmation)
            return f"{feedback}\n\nWhat else would you like to order? (Type 'done' to finish)"
        
        # Parse order input
        feedback, new_order = parse_and_search_order(user_input, restaurants)
        if new_order:
            for order_key, qty in new_order.items():
                if order_key in order:
                    order[order_key] += qty
                else:
                    order[order_key] = qty
        save_state(session_id, order, restaurants, awaiting_confirmation)
        return f"{feedback}\n\nWhat else would you like to order? (Type 'done' to finish)"
    
    except Exception as e:
        logger.error(f"Unexpected error in order processing: {str(e)}")
        return f"An unexpected error occurred: {str(e)}. Please try again."