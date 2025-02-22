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
        return data.get("restaurants", {})
    except requests.RequestException as e:
        print(f"Failed to fetch menu from API: {e}")
        return {}


# Tool call to fetch user credentials from API
def fetch_user_credentials_from_api(user_id="user1"):
    try:
        url = USERS_API_URL.format(user_id)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch user credentials from API: {e}")
        return {}


# Function to search menu and parse order using Mistral API
def parse_and_search_order(user_input, restaurants):
    # Flatten all menu items into a single list for Mistral
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
                "content": "Please provide a concise answer in English. Output the response in the requested format. Do not explain the output. Do not add anything new",
            },
            {"role": "user", "content": [{"type": "text", "text": prompt}]},
        ]

        chat_response = client.chat.complete(model=model, messages=messages)
        result = json.loads(chat_response.choices[0].message.content)

        if "error" in result:
            return None, result["error"]

        order = {}
        messages = []
        for order_item in result:
            item_name = order_item["item"]
            qty = order_item["quantity"]

            # Search across all restaurants
            found = False
            for rest_id, rest_data in restaurants.items():
                for item_id, item in rest_data["menu"].items():
                    if item["name"].lower() == item_name.lower():
                        order_key = (
                            f"{rest_id}:{item_id}"  # Unique key: restaurant_id:item_id
                        )
                        order[order_key] = qty
                        messages.append(
                            f"Added {qty} x {item['name']} (from {rest_data['name']}) to your order."
                        )
                        found = True
                        break
                if found:
                    break
            if not found:
                messages.append(
                    f"Sorry, '{item_name}' is not available at any restaurant."
                )

        return order, "\n".join(messages)

    except Exception as e:
        return None, f"Error processing your order: {str(e)}"


# Function to get delivery details from API
def get_delivery_details(user_id="user1"):
    credentials = fetch_user_credentials_from_api(user_id)
    if not credentials:
        print("No user credentials found. Cannot proceed with delivery.")
        return None

    name = credentials.get("name", "Unknown")
    address = credentials.get("address", "Unknown Address")
    phone = credentials.get("phone", "Unknown Phone")

    print(f"\nAuto-populated delivery details:")
    print(f"Name: {name}")
    print(f"Address: {address}")
    print(f"Phone: {phone}")

    return {"name": name, "address": address, "phone": phone}


# Function to process the order
def process_order(order, details, restaurants):
    if not order:
        print("\nNo items in your order. Goodbye!")
        return

    print("\n=== Order Summary ===")
    total = 0
    for order_key, qty in order.items():
        rest_id, item_id = order_key.split(":")
        item = restaurants[rest_id]["menu"][item_id]
        rest_name = restaurants[rest_id]["name"]
        cost = item["price"] * qty
        total += cost
        print(f"{item['name']} x{qty} (from {rest_name}) - ₹{cost}")
    print(f"Total: ₹{total}")
    print(f"Delivery to: {details['name']}, {details['address']}, {details['phone']}")
    print("=====================\n")

    print("Processing your order...")
    time.sleep(2)
    print("Order placed successfully! You'll receive a confirmation soon.")


# Function to check if all items are from a single restaurant
def is_single_restaurant(order):
    if not order:
        return True
    restaurant_ids = {order_key.split(":")[0] for order_key in order.keys()}
    return len(restaurant_ids) == 1


# Main function to run the bot
def main():
    print("Welcome to the Food Order Bot!")
    print("Loading restaurant data from API...\n")

    # Fetch all restaurants and their menus
    restaurants = fetch_menu_from_api()
    if not restaurants:
        print("Unable to proceed without restaurant data. Exiting.")
        return

    order = {}

    # Take order via natural language input without showing the menu
    while True:
        user_input = input(
            "What would you like to order? (or 'done' to finish): "
        ).strip()
        if user_input.lower() == "done":
            break

        new_order, message = parse_and_search_order(user_input, restaurants)
        print(message)
        if new_order:
            for order_key, qty in new_order.items():
                if order_key in order:
                    order[order_key] += qty  # Add to existing quantity
                else:
                    order[order_key] = qty

    # Process order with restaurant check
    if order:
        if is_single_restaurant(order):
            details = get_delivery_details()
            if details:
                process_order(order, details, restaurants)
            else:
                print("Cannot process order without delivery details.")
        else:
            print("\nYour order contains items from multiple restaurants:")
            total = 0
            for order_key, qty in order.items():
                rest_id, item_id = order_key.split(":")
                item = restaurants[rest_id]["menu"][item_id]
                rest_name = restaurants[rest_id]["name"]
                cost = item["price"] * qty
                total += cost
                print(f"{item['name']} x{qty} (from {rest_name}) - ₹{cost}")
            print(f"Total: ₹{total}")

            confirm = (
                input(
                    "Typically, orders are from a single restaurant. Confirm order? (yes/no): "
                )
                .strip()
                .lower()
            )
            if confirm == "yes":
                details = get_delivery_details()
                if details:
                    process_order(order, details, restaurants)
                else:
                    print("Cannot process order without delivery details.")
            else:
                print("Order cancelled. Please order from a single restaurant.")
    else:
        print("No order to process. Thanks for visiting!")


if __name__ == "__main__":
    main()
