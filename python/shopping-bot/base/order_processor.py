from logging_config import setup_logging
from db import save_order, load_order, save_state, load_state
from config import config
import httpx
from typing import Dict, Optional, List
from models import OrderItem, OrderRequest
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

def filter_restaurants_by_city(restaurants: Dict, city: str) -> Dict:
    """Filter restaurants by city (default to Bengaluru if not specified)."""
    if not city or city.lower() == "bengaluru":
        return restaurants  # All restaurants are in Bengaluru by default
    available_cities = {"New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Bengaluru"}
    if city.lower() not in available_cities:
        return {}
    # Simulate filtering (in real app, use a DB or API to filter by city)
    filtered = {}
    for rest_id, rest_data in restaurants.items():
        if rest_data.get("city", "Bengaluru").lower() == city.lower():
            filtered[rest_id] = rest_data
    return filtered

async def execute_tool_call(tool_call, session_data: Dict, restaurants_data: Dict) -> str:
    function_name = tool_call.function.name
    try:
        arguments = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse tool call arguments: {str(e)}")
        return "Sorry, I couldn’t understand the command arguments. Please try again."

    order = session_data.get("order", {})
    restaurants = session_data.get("restaurants", restaurants_data)
    user_id = session_data.get("user_id")
    token = session_data.get("token")
    selected_restaurant = session_data.get("selected_restaurant")
    session_id = session_data.get("session_id")
    
    logger.info(f"Executing tool call: {function_name} with arguments {arguments}")

    async with httpx.AsyncClient() as client:
        try:
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
                city = arguments.get("city", "Bengaluru")
                filtered_restaurants = filter_restaurants_by_city(restaurants, city)
                if not filtered_restaurants:
                    return f"Sorry, no restaurants available in {city}."
                open_list = "\n".join([f"- {data['name']} ({data.get('opening_hours', 'Hours not specified')})" for data in filtered_restaurants.values()])
                logger.info(f"Listed {len(filtered_restaurants)} open restaurants in {city}")
                return f"Currently open restaurants in {city}:\n{open_list}"

            if function_name == "list_cities":
                cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Bengaluru"]
                city_list = "\n".join([f"- {city}" for city in cities])
                return f"We are currently operational in:\n{city_list}"

            if function_name == "show_menu":
                restaurant_name = arguments.get("restaurant_name")
                city = arguments.get("city", "Bengaluru")
                filtered_restaurants = filter_restaurants_by_city(restaurants, city)
                if restaurant_name:
                    filtered_restaurants = {
                        rest_id: data for rest_id, data in filtered_restaurants.items()
                        if data["name"].lower() == restaurant_name.lower()
                    }
                    if not filtered_restaurants:
                        return f"Sorry, '{restaurant_name}' is not found or not open in {city}."
                return display_menu(filtered_restaurants or restaurants)

            if function_name == "add_to_order":
                item_name = arguments["item_name"]
                quantity = arguments.get("quantity", 1)
                restaurant_name = arguments.get("restaurant_name")
                city = arguments.get("city", "Bengaluru")
                # Filter restaurants by city
                filtered_restaurants = filter_restaurants_by_city(restaurants, city)
                if restaurant_name:
                    filtered_restaurants = {
                        rest_id: data for rest_id, data in filtered_restaurants.items()
                        if data["name"].lower() == restaurant_name.lower()
                    }
                if not filtered_restaurants:
                    return f"Sorry, no matching restaurants found in {city}. Please specify a valid restaurant."

                # Use process_order API to add the item
                user_input = f"{quantity} {item_name}"
                if restaurant_name:
                    user_input += f" from {restaurant_name}"
                response = await client.post(
                    f"{config.BASE_URL}/process_order",
                    json={"session_id": session_id, "user_input": user_input, "token": token},
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code != 200:
                    return f"Error adding item: {response.text}. Please try again."
                return response.text

            if function_name == "remove_from_order":
                item_name = arguments["item_name"]
                response = await client.post(
                    f"{config.BASE_URL}/process_order",
                    json={"session_id": session_id, "user_input": f"remove {item_name}", "token": token},
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code != 200:
                    return f"Error removing item: {response.text}. Please try again."
                return response.text

            if function_name == "show_order":
                response = await client.post(
                    f"{config.BASE_URL}/process_order",
                    json={"session_id": session_id, "user_input": "show order", "token": token},
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code != 200:
                    return f"Error showing order: {response.text}. Please try again."
                return response.text

            if function_name == "review_order":
                response = await client.post(
                    f"{config.BASE_URL}/process_order",
                    json={"session_id": session_id, "user_input": "done", "token": token},
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code != 200:
                    return f"Error reviewing order: {response.text}. Please try again."
                return response.text

            if function_name == "confirm_order":
                response = await client.post(
                    f"{config.BASE_URL}/process_order",
                    json={"session_id": session_id, "user_input": "confirm", "token": token},
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code != 200:
                    return f"Error confirming order: {response.text}. Please try again."
                return response.text

            if function_name == "cancel_order":
                response = await client.post(
                    f"{config.BASE_URL}/process_order",
                    json={"session_id": session_id, "user_input": "cancel", "token": token},
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code != 200:
                    return f"Error cancelling order: {response.text}. Please try again."
                return response.text

            return f"Unknown command: {function_name}. Please try again."
        except Exception as e:
            logger.error(f"Error executing tool call {function_name}: {str(e)}")
            return f"Error processing {function_name}: {str(e)}. Please try again."

async def process_order(session_id: str, user_input: str, username: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None, restaurants_data: Dict = None) -> str:
    # Convert tuple from load_state to a dictionary
    order, restaurants, awaiting_confirmation, user_id, saved_token, selected_restaurant, order_id = load_state(session_id)
    session_data = {
        "order": order,
        "restaurants": restaurants,
        "awaiting_confirmation": awaiting_confirmation,
        "user_id": user_id,
        "token": saved_token,
        "selected_restaurant": selected_restaurant,
        "order_id": order_id,
        "session_id": session_id
    }
    
    if token:
        session_data["token"] = token
    if username:
        session_data["user_id"] = username

    try:
        content, tool_calls = await process_with_tools(user_input, session_data)
    except Exception as e:
        logger.error(f"Unexpected error in process_with_tools: {str(e)}")
        return f"Sorry, an unexpected error occurred: {str(e)}. Please try again."

    if not tool_calls:
        return content
    
    final_response = []
    for tool_call in tool_calls:
        result = await execute_tool_call(tool_call, session_data, restaurants_data)
        final_response.append(result)
    
    return "\n".join(final_response) if final_response else content