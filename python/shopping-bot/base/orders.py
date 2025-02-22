import bleach
from datetime import datetime
import logging
from typing import Dict, Optional
from db import load_state, save_state
from api import fetch_menu_from_api, authenticate, fetch_user_credentials_from_api, submit_order, is_restaurant_open  # Import is_restaurant_open
from llm import parse_and_search_order

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("food_order_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def generate_order_summary(order: Dict, restaurants: Dict) -> str:
    if not order:
        return "No items in your order."
    summary = ["=== Current Order ==="]
    total = 0.0
    for order_key, qty in order.items():
        rest_id, category, item_id = order_key.split(":")
        item = next(i for i in restaurants[rest_id]["menu"][category] if i["id"] == item_id)
        cost = item["price"] * qty
        total += cost
        summary.append(f"{item['name']} x{qty} (from {restaurants[rest_id]['name']}) - ${cost:.2f}")
    summary.append(f"Total: ${total:.2f}")
    return "\n".join(summary)

def remove_item_from_order(item_name: str, order: Dict, restaurants: Dict) -> str:
    item_name_lower = item_name.lower()
    for order_key, qty in list(order.items()):
        rest_id, category, item_id = order_key.split(":")
        item = next(i for i in restaurants[rest_id]["menu"][category] if i["id"] == item_id)
        if item["name"].lower() == item_name_lower:
            del order[order_key]
            return f"Removed {item['name']} from your order."
    return f"'{item_name}' not found in your order."

def process_order(session_id: str, user_input: str, username: Optional[str] = None, password: Optional[str] = None) -> str:
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
            error, restaurants = fetch_menu_from_api(token)  # Already filtered for open restaurants in api.py
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
            error, restaurants = fetch_menu_from_api(token)  # Already filtered in api.py
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