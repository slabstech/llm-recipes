import time
import requests
from mistralai import Mistral
import json
import logging
import os
import sqlite3
import bleach
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "food_order_bot.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# SQLite setup
DB_FILE = os.getenv("DB_FILE", "zomato_orders.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            order_data TEXT,
            restaurants TEXT,
            awaiting_confirmation INTEGER,
            user_id TEXT,
            token TEXT,
            selected_restaurant TEXT
        )
    """)
    conn.commit()
    conn.close()
    logger.info("SQLite database initialized")

# Initialize database on startup
init_db()

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

# API endpoints from environment variables
MENU_API_URL = os.getenv("MENU_API_URL", "http://localhost:7861/menu")
USERS_API_URL = os.getenv("USERS_API_URL", "http://localhost:7861/users/{}")
LOGIN_API_URL = os.getenv("LOGIN_API_URL", "http://localhost:7861/login")

# Function to check if a restaurant is open based on its hours
def is_restaurant_open(opening_hours):
    now = datetime.now()
    current_time = now.hour * 60 + now.minute  # Convert to minutes since midnight
    
    # Parse opening_hours (e.g., "12midnight – 1am, 6am – 12midnight")
    periods = opening_hours.split(", ")
    for period in periods:
        start_str, end_str = period.split(" – ")
        
        def parse_time(time_str):
            time_str = time_str.lower()
            is_pm = "pm" in time_str
            time_str = time_str.replace("am", "").replace("pm", "").replace("midnight", "0").replace("noon", "12")
            hour = int(time_str)
            if is_pm and hour != 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
            return hour * 60
        
        start_minutes = parse_time(start_str)
        end_minutes = parse_time(end_str)
        if end_minutes < start_minutes:  # Overnight period
            end_minutes += 24 * 60
        
        if current_time >= start_minutes and (current_time <= end_minutes or current_time <= end_minutes - 24 * 60):
            return True
    return False

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
        response = requests.get(MENU_API_URL, timeout=5, verify=False)
        response.raise_for_status()
        data = response.json()
        restaurants = data.get("restaurants", {})
        # Filter open restaurants
        open_restaurants = {}
        for rest_id, rest_data in restaurants.items():
            if "opening_hours" in rest_data and is_restaurant_open(rest_data["opening_hours"]):
                open_restaurants[rest_id] = rest_data
        logger.info(f"Successfully fetched menu. Open restaurants: {len(open_restaurants)}")
        return None, open_restaurants
    except requests.RequestException as e:
        logger.error(f"Failed to fetch menu from API: {str(e)}")
        raise

# Function to authenticate and get token with retry
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=lambda retry_state: logger.info(f"Retrying authenticate: attempt {retry_state.attempt_number}")
)
def authenticate(username, password):
    logger.info(f"Attempting to authenticate user: {username}")
    try:
        response = requests.post(
            LOGIN_API_URL,
            json={"username": username, "password": password},
            timeout=5,
            verify=False
        )
        response.raise_for_status()
        token = response.json().get("access_token")
        logger.info(f"Successfully authenticated user {username} and received token")
        return token
    except requests.RequestException as e:
        logger.error(f"Failed to authenticate user {username}: {str(e)}")
        raise

# Tool call to fetch user credentials from API with retry and authentication
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(requests.RequestException),
    before_sleep=lambda retry_state: logger.info(f"Retrying fetch_user_credentials_from_api: attempt {retry_state.attempt_number}")
)
def fetch_user_credentials_from_api(user_id, token):
    logger.info(f"Fetching user credentials for user_id: {user_id}")
    try:
        url = USERS_API_URL.format(user_id)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        response.raise_for_status()
        logger.info(f"Successfully fetched user credentials for {user_id}")
        return None, response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch user credentials: {str(e)}")
        raise

# Function to search menu and parse order with restaurant restriction
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(Exception),
    before_sleep=lambda retry_state: logger.info(f"Retrying parse_and_search_order: attempt {retry_state.attempt_number}")
)
def parse_and_search_order(user_input, restaurants, selected_restaurant=None):
    logger.info(f"Parsing order input: {user_input} with selected restaurant: {selected_restaurant}")
    try:
        all_items = []
        item_map = {}
        for rest_id, rest_data in restaurants.items():
            for category, items in rest_data["menu"].items():
                for item in items:
                    item_name = item["name"]
                    all_items.append(f"{item_name} (from {rest_data['name']})")
                    item_map[item_name.lower()] = {
                        "rest_id": rest_id,
                        "category": category,
                        "item_id": item["id"]
                    }
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
            {"role": "system", "content": "Please provide a concise answer in English. Output the response in the requested format. Do not explain the output. Do not add anything new"},
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
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
            
            item_key = item_name.lower()
            if item_key in item_map:
                details = item_map[item_key]
                rest_id = details["rest_id"]
                if selected_restaurant and rest_id != selected_restaurant:
                    feedback.append(f"Sorry, '{item_name}' is from {restaurants[rest_id]['name']}. You can only order from {restaurants[selected_restaurant]['name']} in this session.")
                    continue
                category = details["category"]
                item_id = details["item_id"]
                order_key = f"{rest_id}:{category}:{item_id}"
                order[order_key] = qty
                
                rest_name = restaurants[rest_id]["name"]
                feedback.append(f"Added {qty} x {item_name} (from {rest_name}) to your order.")
            else:
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
        rest_id, category, item_id = order_key.split(":")
        rest_data = restaurants[rest_id]
        item = next(i for i in rest_data["menu"][category] if i["id"] == item_id)
        rest_name = rest_data["name"]
        cost = item["price"] * qty
        total += cost
        summary.append(f"{item['name']} x{qty} (from {rest_name}) - ₹{cost}")
    summary.append(f"Total: ₹{total}")
    return "\n".join(summary)

# Function to remove an item from the order
def remove_item_from_order(item_name, order, restaurants):
    logger.info(f"Attempting to remove item: {item_name}")
    item_name_lower = item_name.lower()
    for order_key, qty in list(order.items()):
        rest_id, category, item_id = order_key.split(":")
        rest_data = restaurants[rest_id]
        item = next(i for i in rest_data["menu"][category] if i["id"] == item_id)
        if item["name"].lower() == item_name_lower:
            del order[order_key]
            logger.info(f"Removed {item['name']} from order")
            return f"Removed {item['name']} from your order."
    logger.warning(f"Item not found in order: {item_name}")
    return f"'{item_name}' not found in your order."

# Functions to manage state in SQLite
def save_state(session_id, order, restaurants, awaiting_confirmation, user_id=None, token=None, selected_restaurant=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (session_id, order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            json.dumps(order),
            json.dumps(restaurants),
            int(awaiting_confirmation),
            user_id,
            token,
            selected_restaurant
        ))
        conn.commit()
        logger.info(f"Saved state for session {session_id}")
    except sqlite3.Error as e:
        logger.error(f"Failed to save state to SQLite: {str(e)}")
    finally:
        conn.close()

def load_state(session_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant FROM sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        if result:
            order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant = result
            return json.loads(order), json.loads(restaurants), bool(awaiting_confirmation), user_id, token, selected_restaurant
        logger.info(f"No state found for session {session_id}, initializing new state")
        return {}, {}, False, None, None, None
    except sqlite3.Error as e:
        logger.error(f"Failed to load state from SQLite: {str(e)}")
        return {}, {}, False, None, None, None
    finally:
        conn.close()

# Core order processing logic with SQLite state, authentication, and input validation
def process_order(session_id, user_input, username=None, password=None):
    logger.info(f"Processing user input for session {session_id}: {user_input}")
    order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant = load_state(session_id)
    
    if not restaurants:
        error, loaded_restaurants = fetch_menu_from_api()
        if error:
            return error
        restaurants = loaded_restaurants
        if not restaurants:
            return "No restaurants are currently open."
        save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant)
    
    # Input validation and sanitization
    if not user_input or user_input.isspace():
        logger.warning("Empty or whitespace-only input received")
        return "Please provide a valid input."
    user_input = bleach.clean(user_input.strip().lower())
    
    try:
        # Handle login command
        if user_input.startswith("login "):
            parts = user_input.split(" ", 2)
            if len(parts) != 3:
                logger.warning("Invalid login command format")
                return "Please provide username and password (e.g., 'login user1 password123')."
            username, password = parts[1], parts[2]
            if not username or not password or len(username) > 50 or len(password) > 50:
                logger.warning("Invalid username or password length")
                return "Username and password must be non-empty and less than 50 characters."
            token = authenticate(username, password)
            if not token:
                return "Login failed. Invalid credentials."
            user_id = username
            open_list = "\n".join([f"- {data['name']} ({', '.join(data['cuisine'])})" for data in restaurants.values()])
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant)
            return f"Logged in as {user_id}. Here are the open restaurants:\n{open_list}\nWhat would you like to order?"
        
        # Require login for most commands
        if not user_id and user_input not in ["login"]:
            return "Please log in first (e.g., 'login user1 password123')."
        
        # Handle "list restaurants" command
        if user_input == "list restaurants":
            open_list = "\n".join([f"- {data['name']} ({', '.join(data['cuisine'])})" for data in restaurants.values()])
            return f"Currently open restaurants:\n{open_list}"
        
        # Handle confirmation for multi-restaurant orders (shouldn't occur with new logic, kept for compatibility)
        if awaiting_confirmation:
            if user_input in ["yes", "y"]:
                if not token:
                    token = authenticate(username, password)
                    if not token:
                        return "Authentication failed. Unable to process order."
                error, credentials = fetch_user_credentials_from_api(user_id, token)
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
                save_state(session_id, {}, restaurants, False, user_id, token, None)
                return response
            elif user_input in ["no", "n"]:
                logger.info("Order cancelled by user")
                response = "Order cancelled. What would you like to order next?"
                save_state(session_id, {}, restaurants, False, user_id, token, None)
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
            if not token:
                token = authenticate(username, password)
                if not token:
                    return "Authentication failed. Unable to process order."
            error, credentials = fetch_user_credentials_from_api(user_id, token)
            if error:
                logger.error(f"Cannot proceed due to: {error}")
                return error
            
            name = credentials.get("name", "Unknown")
            address = credentials.get("address", "Unknown Address")
            phone = credentials.get("phone", "Unknown Phone")
            delivery_info = f"Delivery to: {name}, {address}, {phone}"
            logger.info("Order processed successfully")
            response = f"{summary}\n{delivery_info}\n\nProcessing your order...\nOrder placed successfully! You'll receive a confirmation soon."
            save_state(session_id, {}, restaurants, False, user_id, token, None)
            return response
        
        # Handle "show order" command
        if user_input == "show order":
            summary = generate_order_summary(order, restaurants)
            logger.info("Showing current order")
            return summary
        
        # Handle "remove [item]" command
        if user_input.startswith("remove "):
            item_name = user_input.replace("remove ", "").strip()
            if not item_name:
                logger.warning("No item specified for removal")
                return "Please specify an item to remove (e.g., 'remove Butter Idli')."
            if len(item_name) > 50:
                logger.warning("Item name too long")
                return "Item name must be less than 50 characters."
            feedback = remove_item_from_order(item_name, order, restaurants)
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant)
            return feedback
        
        # Parse order input
        if len(user_input) > 200:
            logger.warning("Order input too long")
            return "Order input must be less than 200 characters."
        feedback, new_order = parse_and_search_order(user_input, restaurants, selected_restaurant)
        if new_order:
            if not selected_restaurant and new_order:
                # Set the selected restaurant based on the first item ordered
                selected_restaurant = list(new_order.keys())[0].split(":")[0]
                logger.info(f"Selected restaurant set to: {restaurants[selected_restaurant]['name']}")
            for order_key, qty in new_order.items():
                if order_key in order:
                    order[order_key] += qty
                else:
                    order[order_key] = qty
        save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant)
        return f"{feedback}\n\nWhat else would you like to order from {restaurants[selected_restaurant]['name']}? (Type 'done' to finish)"
    
    except Exception as e:
        logger.error(f"Unexpected error in order processing: {str(e)}")
        return f"An unexpected error occurred: {str(e)}. Please try again."