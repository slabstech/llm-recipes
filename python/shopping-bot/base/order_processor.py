from logging_config import setup_logging
from db import save_order, load_order, save_state, load_state
from config import config
import httpx
from typing import Dict, Optional, List
from models import OrderItem, OrderRequest  # Import from models
from llm import process_with_tools
import json
logger = setup_logging(__name__)

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
            logger.info(f"Removed item '{item_name}' from order")
            return f"Removed {item['name']} from your order."
    logger.warning(f"Item '{item_name}' not found in order")
    return f"'{item_name}' not found in your order."

def display_menu(restaurants: Dict) -> str:
    if not restaurants:
        return "No open restaurants available to display a menu."
    menu_lines = ["=== Available Menu ==="]
    for rest_id, rest_data in restaurants.items():
        menu_lines.append(f"\n{rest_data['name']} ({rest_data.get('opening_hours', 'Hours not specified')})")
        for category, items in rest_data["menu"].items():
            menu_lines.append(f"  {category}:")
            for item in items:
                menu_lines.append(f"    - {item['name']} (${item['price']:.2f})")
    menu_lines.append("\nType an order like '1 Butter Idli' or 'list restaurants' to continue.")
    logger.info(f"Displayed menu for {len(restaurants)} restaurants")
    return "\n".join(menu_lines)

async def execute_tool_call(tool_call, session_data: Dict, restaurants_data: Dict) -> str:
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    order = session_data.get("order", {})
    restaurants = session_data.get("restaurants", restaurants_data)
    user_id = session_data.get("user_id")
    token = session_data.get("token")
    selected_restaurant = session_data.get("selected_restaurant")
    session_id = session_data.get("session_id")
    
    logger.info(f"Executing tool call: {function_name} with arguments {arguments}")

    async with httpx.AsyncClient() as client:
        if function_name == "login":
            username = arguments["username"]
            password = arguments["password"]
            response = await client.post(
                config.LOGIN_API_URL,
                json={"username": username, "password": password}
            )
            if response.status_code != 200:
                return "Login failed. Please check your username and password and try again."
            token_response = response.json()
            token = token_response["access_token"]
            response = await client.get(config.MENU_API_URL, headers={"Authorization": f"Bearer {token}"})
            if response.status_code != 200:
                return f"Login succeeded, but I couldn't load the menu. Please try again later or contact support if this persists."
            data = response.json()
            restaurants = data.get("restaurants", {})
            user_id = username
            open_list = "\n".join([f"- {data['name']} ({data.get('opening_hours', 'Hours not specified')})" for data in restaurants.values()])
            save_state(session_id, order, restaurants, False, user_id, token, selected_restaurant, None)
            logger.info(f"User {user_id} logged in successfully")
            return f"Logged in as {user_id}. Open restaurants:\n{open_list}\nWhat would you like to order?"

        if not user_id or not token:
            return "Please log in first by saying 'login <username> <password>' (e.g., 'login user1 password123')."

        if function_name == "list_restaurants":
            open_list = "\n".join([f"- {data['name']} ({data.get('opening_hours', 'Hours not specified')})" for data in restaurants.values()])
            logger.info(f"Listed {len(restaurants)} open restaurants")
            return f"Currently open restaurants:\n{open_list}"

        if function_name == "show_menu":
            return display_menu(restaurants)

        if function_name == "add_to_order":
            item_name = arguments["item_name"]
            quantity = arguments.get("quantity", 1)
            from llm import parse_and_search_order  # Local import to avoid circularity
            feedback, new_order = parse_and_search_order(f"{quantity} {item_name}", restaurants, selected_restaurant)
            if new_order:
                if not selected_restaurant:
                    selected_restaurant = list(new_order.keys())[0].split(":")[0]
                for order_key, qty in new_order.items():
                    order[order_key] = order.get(order_key, 0) + qty
                logger.info(f"Added items to order: {new_order}")
                save_state(session_id, order, restaurants, False, user_id, token, selected_restaurant, None)
            return feedback

        if function_name == "remove_from_order":
            item_name = arguments["item_name"]
            feedback = remove_item_from_order(item_name, order, restaurants)
            save_state(session_id, order, restaurants, False, user_id, token, selected_restaurant, None)
            return feedback

        if function_name == "show_order":
            return generate_order_summary(order, restaurants)

        if function_name == "review_order":
            if not order:
                return "You haven't added any items to your order yet. What would you like to order?"
            summary = generate_order_summary(order, restaurants)
            logger.info(f"Order review requested for session {session_id}")
            return f"{summary}\nPlease say 'confirm' to place your order or 'cancel' to discard it."

        if function_name == "confirm_order":
            if not order:
                return "There's no order to confirm. Please add items to your order first."
            summary = generate_order_summary(order, restaurants)
            response = await client.get(config.USERS_API_URL.format(user_id), headers={"Authorization": f"Bearer {token}"})
            if response.status_code != 200:
                return "I couldn't process your order because I can't retrieve your details. Please try again or log out and back in."
            credentials = response.json().get("data", {})
            order_request = OrderRequest(items=[
                OrderItem(
                    item_id=key.split(":")[2],
                    quantity=qty,
                    restaurant_id=key.split(":")[0],
                    category=key.split(":")[1]
                ) for key, qty in order.items()
            ])
            order_response = await client.post(config.ORDERS_API_URL, json=order_request.dict(), headers={"Authorization": f"Bearer {token}"})
            if order_response.status_code != 200:
                return "Sorry, there was an issue placing your order. Please try again or contact support if this continues."
            order_data = order_response.json()
            name = credentials.get("name", "Unknown")
            address = credentials.get("address", "Unknown Address")
            phone = credentials.get("phone", "Unknown Phone")
            delivery_info = f"Delivery to: {name}, {address}, {phone}"
            response = f"{summary}\n{delivery_info}\n\nOrder placed successfully! Order ID: {order_data['order_id']}"
            save_state(session_id, {}, restaurants, False, user_id, token, None, order_data['order_id'])
            logger.info(f"Order confirmed for session {session_id}, Order ID: {order_data['order_id']}")
            return response

        if function_name == "cancel_order":
            if not order:
                return "There's no order to cancel."
            order.clear()
            save_state(session_id, order, restaurants, False, user_id, token, None, None)
            logger.info(f"Order cancelled for session {session_id}")
            return "Your order has been cancelled. What would you like to order next?"

        return f"Unknown command: {function_name}. Please try again."

async def process_order(session_id: str, user_input: str, username: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None, restaurants_data: Dict = None) -> str:
    session_data = load_state(session_id)
    session_data["session_id"] = session_id
    if token:
        session_data["token"] = token
    if username:
        session_data["user_id"] = username

    content, tool_calls = await process_with_tools(user_input, session_data)
    
    if not tool_calls:
        return content
    
    final_response = []
    for tool_call in tool_calls:
        result = await execute_tool_call(tool_call, session_data, restaurants_data)
        final_response.append(result)
    
    return "\n".join(final_response) if final_response else content