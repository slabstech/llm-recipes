import time
import requests
from mistralai import Mistral
import json
import logging
import os

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

# API endpoints from the Flask mock server
#MENU_API_URL = "http://localhost:5000/menu"
#USERS_API_URL = "http://localhost:5000/users/{}"

## hosted on HF spaces
MENU_API_URL = "https://gaganyatri-mock-restaurant-api.hf.space/menu"
USERS_API_URL = "https://gaganyatri-mock-restaurant-api.hf.space/users/{}"

# Tool call to fetch all restaurants and their menus from API
def fetch_menu_from_api():
    logger.info("Fetching menu from API")
    try:
        response = requests.get(MENU_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        logger.info("Successfully fetched menu")
        return None, data.get("restaurants", {})
    except requests.RequestException as e:
        logger.error(f"Failed to fetch menu from API: {str(e)}")
        return f"Failed to fetch menu from API: {str(e)}", {}

# Tool call to fetch user credentials from API
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
        return f"Failed to fetch user credentials from API: {str(e)}", {}

# Function to search menu and parse order using Mistral API
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
        return f"Error parsing order response: {str(e)}", {}
    except Exception as e:
        logger.error(f"Error processing order with Mistral API: {str(e)}")
        return f"Error processing your order: {str(e)}", {}

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
    for order_key, qty in list(order.items()):  # Use list to avoid runtime dict modification
        rest_id, item_id = order_key.split(":")
        item = restaurants[rest_id]["menu"][item_id]
        if item["name"].lower() == item_name:
            del order[order_key]
            logger.info(f"Removed {item['name']} from order")
            return f"Removed {item['name']} from your order."
    logger.warning(f"Item not found in order: {item_name}")
    return f"'{item_name}' not found in your order."

# Core order processing logic
def process_order(user_input, order, restaurants, awaiting_confirmation):
    logger.info(f"Processing user input: {user_input}")
    if not restaurants:
        logger.error("No restaurant data available")
        return "Failed to load restaurant data. Please try again later.", order, False
    
    user_input = user_input.strip().lower()
    
    try:
        # Handle confirmation for multi-restaurant orders
        if awaiting_confirmation:
            if user_input in ["yes", "y"]:
                error, credentials = fetch_user_credentials_from_api()
                if error:
                    logger.error(f"Cannot proceed due to: {error}")
                    return error, order, False
                
                name = credentials.get("name", "Unknown")
                address = credentials.get("address", "Unknown Address")
                phone = credentials.get("phone", "Unknown Phone")
                summary = generate_order_summary(order, restaurants)
                delivery_info = f"Delivery to: {name}, {address}, {phone}"
                logger.info("Order confirmed and processed successfully")
                return f"{summary}\n{delivery_info}\n\nProcessing your order...\nOrder placed successfully! You'll receive a confirmation soon.", {}, False
            elif user_input in ["no", "n"]:
                logger.info("Order cancelled by user")
                return "Order cancelled. Please order from a single restaurant. What would you like to order next?", {}, False
            else:
                logger.warning(f"Invalid confirmation response: {user_input}")
                return "Please respond with 'yes' or 'no' to confirm the order.", order, True
        
        # Handle "done" command
        if user_input == "done":
            if not order:
                logger.info("No items in order when 'done' received")
                return "No order to process. What would you like to order?", order, False
            
            summary = generate_order_summary(order, restaurants)
            if is_single_restaurant(order):
                error, credentials = fetch_user_credentials_from_api()
                if error:
                    logger.error(f"Cannot proceed due to: {error}")
                    return error, order, False
                
                name = credentials.get("name", "Unknown")
                address = credentials.get("address", "Unknown Address")
                phone = credentials.get("phone", "Unknown Phone")
                delivery_info = f"Delivery to: {name}, {address}, {phone}"
                logger.info("Order processed successfully from single restaurant")
                return f"{summary}\n{delivery_info}\n\nProcessing your order...\nOrder placed successfully! You'll receive a confirmation soon.", {}, False
            else:
                logger.info("Order contains items from multiple restaurants")
                return f"{summary}\n\nYour order contains items from multiple restaurants. Typically, orders are from a single restaurant. Confirm order? (yes/no)", order, True
        
        # Handle "show order" command
        if user_input == "show order":
            summary = generate_order_summary(order, restaurants)
            logger.info("Showing current order")
            return f"{summary}\n\nWhat else would you like to order? (Type 'done' to finish)", order, False
        
        # Handle "remove [item]" command
        if user_input.startswith("remove "):
            item_name = user_input.replace("remove ", "").strip()
            if not item_name:
                logger.warning("No item specified for removal")
                return "Please specify an item to remove (e.g., 'remove butter chicken').", order, False
            feedback = remove_item_from_order(item_name, order, restaurants)
            return f"{feedback}\n\nWhat else would you like to order? (Type 'done' to finish)", order, False
        
        # Parse order input
        feedback, new_order = parse_and_search_order(user_input, restaurants)
        if new_order:
            for order_key, qty in new_order.items():
                if order_key in order:
                    order[order_key] += qty
                else:
                    order[order_key] = qty
        return f"{feedback}\n\nWhat else would you like to order? (Type 'done' to finish)", order, False
    
    except Exception as e:
        logger.error(f"Unexpected error in order processing: {str(e)}")
        return f"An unexpected error occurred: {str(e)}. Please try again.", order, False