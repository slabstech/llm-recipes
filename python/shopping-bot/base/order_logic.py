import time
import requests
from mistralai import Mistral
import json
import os 
# Mistral API key (replace with your own from mistral.ai)

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

# API endpoints from the Flask mock server
MENU_API_URL = "http://localhost:5000/menu"
USERS_API_URL = "http://localhost:5000/users/{}"

# Tool call to fetch all restaurants and their menus from API
def fetch_menu_from_api():
    try:
        response = requests.get(MENU_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return None, data.get("restaurants", {})
    except requests.RequestException as e:
        return f"Failed to fetch menu from API: {e}", {}

# Tool call to fetch user credentials from API
def fetch_user_credentials_from_api(user_id="user1"):
    try:
        url = USERS_API_URL.format(user_id)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return None, response.json()
    except requests.RequestException as e:
        return f"Failed to fetch user credentials from API: {e}", {}

# Function to search menu and parse order using Mistral API
def parse_and_search_order(user_input, restaurants):
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
    
    try:
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
        
        return "\n".join(feedback), order
    
    except Exception as e:
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
    
    summary = ["=== Order Summary ==="]
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

# Core order processing logic
def process_order(user_input, order, restaurants, awaiting_confirmation):
    if not restaurants:
        return "Failed to load restaurant data. Please try again later.", order, False
    
    user_input = user_input.strip().lower()
    
    # Handle confirmation for multi-restaurant orders
    if awaiting_confirmation:
        if user_input in ["yes", "y"]:
            error, credentials = fetch_user_credentials_from_api()
            if error:
                return error, order, False
            
            name = credentials.get("name", "Unknown")
            address = credentials.get("address", "Unknown Address")
            phone = credentials.get("phone", "Unknown Phone")
            summary = generate_order_summary(order, restaurants)
            delivery_info = f"Delivery to: {name}, {address}, {phone}"
            return f"{summary}\n{delivery_info}\n\nProcessing your order...\nOrder placed successfully! You'll receive a confirmation soon.", {}, False
        elif user_input in ["no", "n"]:
            return "Order cancelled. Please order from a single restaurant. What would you like to order next?", {}, False
        else:
            return "Please respond with 'yes' or 'no' to confirm the order.", order, True
    
    # Handle "done" command
    if user_input == "done":
        if not order:
            return "No order to process. What would you like to order?", order, False
        
        summary = generate_order_summary(order, restaurants)
        if is_single_restaurant(order):
            error, credentials = fetch_user_credentials_from_api()
            if error:
                return error, order, False
            
            name = credentials.get("name", "Unknown")
            address = credentials.get("address", "Unknown Address")
            phone = credentials.get("phone", "Unknown Phone")
            delivery_info = f"Delivery to: {name}, {address}, {phone}"
            return f"{summary}\n{delivery_info}\n\nProcessing your order...\nOrder placed successfully! You'll receive a confirmation soon.", {}, False
        else:
            return f"{summary}\n\nYour order contains items from multiple restaurants. Typically, orders are from a single restaurant. Confirm order? (yes/no)", order, True
    
    # Parse order input
    feedback, new_order = parse_and_search_order(user_input, restaurants)
    if new_order:
        for order_key, qty in new_order.items():
            if order_key in order:
                order[order_key] += qty
            else:
                order[order_key] = qty
    return f"{feedback}\n\nWhat else would you like to order? (Type 'done' to finish)", order, False