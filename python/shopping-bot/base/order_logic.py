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

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "food_order_bot.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

DB_FILE = os.getenv("DB_FILE", "zomato_orders.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS sessions")
    cursor.execute("""
        CREATE TABLE sessions (
            session_id TEXT PRIMARY KEY,
            order_data TEXT,
            restaurants TEXT,
            awaiting_confirmation INTEGER,
            user_id TEXT,
            token TEXT,
            selected_restaurant TEXT,
            order_id TEXT
        )
    """)
    conn.commit()
    conn.close()
    logger.info("SQLite database initialized with updated schema")

init_db()

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

BASE_URL = os.getenv("BASE_URL", "http://localhost:7861")
MENU_API_URL = f"{BASE_URL}/menu"
USERS_API_URL = f"{BASE_URL}/users/{{}}"
LOGIN_API_URL = f"{BASE_URL}/login"
ORDERS_API_URL = f"{BASE_URL}/orders"

def is_restaurant_open(opening_hours):
    now = datetime.now()
    current_time = now.hour * 60 + now.minute
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
        if end_minutes < start_minutes:
            end_minutes += 24 * 60
        if current_time >= start_minutes and (current_time <= end_minutes or current_time <= end_minutes - 24 * 60):
            return True
    return False

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def fetch_menu_from_api(token=None):
    logger.info(f"Fetching menu from API: {MENU_API_URL} with token: {token}")
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        logger.debug(f"Sending request with headers: {headers}")
        response = requests.get(MENU_API_URL, headers=headers, timeout=5, verify=False)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"API response: {data}")
        if not data.get("success", False):
            raise ValueError("API response indicates failure")
        restaurants = data.get("restaurants", {})
        open_restaurants = {
            rest_id: rest_data for rest_id, rest_data in restaurants.items()
            if "opening_hours" in rest_data and is_restaurant_open(rest_data["opening_hours"])
        }
        logger.info(f"Successfully fetched menu. Open restaurants: {len(open_restaurants)}")
        return None, open_restaurants
    except requests.RequestException as e:
        logger.error(f"Failed to fetch menu from API: {str(e)} - Response: {e.response.text if e.response else 'No response'}")
        return str(e), {}
    except ValueError as e:
        logger.error(f"API returned invalid data: {str(e)}")
        return str(e), {}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
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
        logger.info(f"Successfully authenticated user {username}. Token: {token}")
        return token
    except requests.RequestException as e:
        logger.error(f"Failed to authenticate user {username}: {str(e)}")
        return None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def fetch_user_credentials_from_api(user_id, token):
    logger.info(f"Fetching user credentials for user_id: {user_id}")
    try:
        url = USERS_API_URL.format(user_id)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        response.raise_for_status()
        logger.info(f"Successfully fetched user credentials for {user_id}")
        return None, response.json().get("data", {})
    except requests.RequestException as e:
        logger.error(f"Failed to fetch user credentials: {str(e)}")
        return str(e), {}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(Exception))
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
        You are a food order bot. The menu items available are: {menu_str}.
        Parse the user's input into a structured order (item names and quantities).
        User input: "{user_input}"
        Respond in JSON format:
        - For valid orders: [{{"item": "item_name", "quantity": number}}, ...]
        - For invalid orders: {{"error": "message"}}
        Match item names exactly (case-insensitive). If no quantity is specified, assume 1.
        """
        logger.debug(f"Sending prompt to Mistral API: {prompt}")
        
        chat_response = client.chat.complete(model="mistral-large-latest", messages=[{"role": "user", "content": prompt}])
        response_content = chat_response.choices[0].message.content.strip()
        logger.debug(f"Mistral API response: {response_content}")
        
        if not response_content:
            raise ValueError("Mistral API returned an empty response")
        
        result = json.loads(response_content)
        
        if "error" in result:
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
                    feedback.append(f"Sorry, '{item_name}' is from {restaurants[rest_id]['name']}. You can only order from {restaurants[selected_restaurant]['name']}.")
                    continue
                category = details["category"]
                item_id = details["item_id"]
                order_key = f"{rest_id}:{category}:{item_id}"
                order[order_key] = qty
                feedback.append(f"Added {qty} x {item_name} (from {restaurants[rest_id]['name']}) to your order.")
            else:
                feedback.append(f"Sorry, '{item_name}' is not available.")
        
        return "\n".join(feedback), order
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Mistral API response as JSON: {str(e)}")
        return f"Error parsing order: Invalid response from API - {str(e)}", {}
    except ValueError as e:
        logger.error(f"Mistral API error: {str(e)}")
        return f"Error parsing order: {str(e)}", {}
    except Exception as e:
        logger.error(f"Unexpected error in parse_and_search_order: {str(e)}")
        return f"Error parsing order: {str(e)}", {}

def generate_order_summary(order, restaurants):
    if not order:
        return "No items in your order."
    summary = ["=== Current Order ==="]
    total = 0
    for order_key, qty in order.items():
        rest_id, category, item_id = order_key.split(":")
        item = next(i for i in restaurants[rest_id]["menu"][category] if i["id"] == item_id)
        cost = item["price"] * qty
        total += cost
        summary.append(f"{item['name']} x{qty} (from {restaurants[rest_id]['name']}) - ${cost:.2f}")
    summary.append(f"Total: ${total:.2f}")
    return "\n".join(summary)

def remove_item_from_order(item_name, order, restaurants):
    item_name_lower = item_name.lower()
    for order_key, qty in list(order.items()):
        rest_id, category, item_id = order_key.split(":")
        item = next(i for i in restaurants[rest_id]["menu"][category] if i["id"] == item_id)
        if item["name"].lower() == item_name_lower:
            del order[order_key]
            return f"Removed {item['name']} from your order."
    return f"'{item_name}' not found in your order."

def save_state(session_id, order, restaurants, awaiting_confirmation, user_id=None, token=None, selected_restaurant=None, order_id=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (session_id, order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            json.dumps(order),
            json.dumps(restaurants),
            int(awaiting_confirmation),
            user_id,
            token,
            selected_restaurant,
            order_id
        ))
        conn.commit()
        logger.info(f"Saved state for session {session_id} with token: {token}")
    except sqlite3.Error as e:
        logger.error(f"Failed to save state: {str(e)}")
    finally:
        conn.close()

def load_state(session_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id FROM sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        if result:
            logger.debug(f"Loaded state for session {session_id}: {result}")
            return (json.loads(result[0]), json.loads(result[1]), bool(result[2]), result[3], result[4], result[5], result[6])
        logger.info(f"No state found for session {session_id}")
        return {}, {}, False, None, None, None, None
    except sqlite3.Error as e:
        logger.error(f"Failed to load state: {str(e)}")
        return {}, {}, False, None, None, None, None
    finally:
        conn.close()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def submit_order(order, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        order_items = [
            {"item_id": key.split(":")[2], "quantity": qty, "restaurant_id": key.split(":")[0], "category": key.split(":")[1]}
            for key, qty in order.items()
        ]
        response = requests.post(ORDERS_API_URL, json={"items": order_items}, headers=headers, timeout=5, verify=False)
        response.raise_for_status()
        return None, response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to submit order: {str(e)}")
        return str(e), {}

def process_order(session_id, user_input, username=None, password=None):
    order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id = load_state(session_id)
    
    user_input = bleach.clean(user_input.strip().lower())
    
    try:
        if user_input.startswith("login "):
            parts = user_input.split(" ", 2)
            if len(parts) != 3:
                return "Please provide username and password (e.g., 'login user1 password123')."
            username, password = parts[1], parts[2]
            token = authenticate(username, password)
            if not token:
                return "Login failed. Invalid credentials."
            logger.debug(f"Token after login: {token}")
            error, restaurants = fetch_menu_from_api(token)
            if error:
                return f"Login successful, but failed to fetch menu: {error}"
            user_id = username
            open_list = "\n".join([f"- {data['name']} ({data.get('opening_hours', 'Hours not specified')})" for data in restaurants.values()])
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
            return f"Logged in as {user_id}. Open restaurants:\n{open_list}\nWhat would you like to order?"
        
        if not user_id:
            return "Please log in first (e.g., 'login user1 password123')."
        
        if not restaurants:
            logger.debug(f"Fetching menu with existing token: {token}")
            error, restaurants = fetch_menu_from_api(token)
            if error:
                return f"Failed to fetch menu: {error}"
            if not restaurants:
                return "No restaurants are currently open."
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
        
        if user_input == "list restaurants":
            open_list = "\n".join([f"- {data['name']} ({data.get('opening_hours', 'Hours not specified')})" for data in restaurants.values()])
            return f"Currently open restaurants:\n{open_list}"
        
        if user_input == "show order":
            return generate_order_summary(order, restaurants)
        
        if user_input.startswith("remove "):
            item_name = user_input.replace("remove ", "").strip()
            if not item_name:
                return "Please specify an item to remove (e.g., 'remove Butter Idli')."
            feedback = remove_item_from_order(item_name, order, restaurants)
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
            return feedback
        
        if user_input == "done":
            if not order:
                return "No order to process. What would you like to order?"
            summary = generate_order_summary(order, restaurants)
            error, credentials = fetch_user_credentials_from_api(user_id, token)
            if error:
                return f"Cannot process order: {error}"
            error, order_response = submit_order(order, token)
            if error:
                return f"Failed to place order: {error}"
            name = credentials.get("name", "Unknown")
            address = credentials.get("address", "Unknown Address")
            phone = credentials.get("phone", "Unknown Phone")
            delivery_info = f"Delivery to: {name}, {address}, {phone}"
            response = f"{summary}\n{delivery_info}\n\nOrder placed successfully! Order ID: {order_response['order_id']}"
            save_state(session_id, {}, restaurants, False, user_id, token, None, order_response['order_id'])
            return response
        
        feedback, new_order = parse_and_search_order(user_input, restaurants, selected_restaurant)
        if new_order:
            if not selected_restaurant:
                selected_restaurant = list(new_order.keys())[0].split(":")[0]
            for order_key, qty in new_order.items():
                order[order_key] = order.get(order_key, 0) + qty
        save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
        return f"{feedback}\n\nWhat else would you like to order from {restaurants[selected_restaurant]['name']}? (Type 'done' to finish)"
    
    except Exception as e:
        logger.error(f"Unexpected error in order processing: {str(e)}")
        return f"An unexpected error occurred: {str(e)}. Please try again."
