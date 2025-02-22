import bleach
from datetime import datetime
import logging
from db import load_state, save_state
from api import fetch_menu_from_api, authenticate, fetch_user_credentials_from_api, submit_order
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
            error, restaurants_data = fetch_menu_from_api(token)
            if error:
                return f"Login successful, but failed to fetch menu: {error}"
            restaurants = {rest_id: rest_data for rest_id, rest_data in restaurants_data.items() if is_restaurant_open(rest_data.get("opening_hours", ""))}
            user_id = username
            open_list = "\n".join([f"- {data['name']} ({data.get('opening_hours', 'Hours not specified')})" for data in restaurants.values()])
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
            return f"Logged in as {user_id}. Open restaurants:\n{open_list}\nWhat would you like to order?"
        
        if not user_id:
            return "Please log in first (e.g., 'login user1 password123')."
        
        if not restaurants:
            logger.debug(f"Fetching menu with existing token: {token}")
            error, restaurants_data = fetch_menu_from_api(token)
            if error:
                return f"Failed to fetch menu: {error}"
            restaurants = {rest_id: rest_data for rest_id, rest_data in restaurants_data.items() if is_restaurant_open(rest_data.get("opening_hours", ""))}
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