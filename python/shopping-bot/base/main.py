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

# Tool call to fetch menu from API
def fetch_menu_from_api():
    try:
        response = requests.get(MENU_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("menu", {})
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

# Function to display the menu
def display_menu(menu):
    if not menu:
        print("No menu available.")
        return
    print("\n=== Zomato Order Bot Menu ===")
    for key, item in menu.items():
        print(f"{key}. {item['name']} - ₹{item['price']}")
    print("============================\n")

# Function to parse order using Mistral API
def parse_order_input(user_input, menu):
    order = {}
    menu_str = ", ".join([f"{item['name']}" for item in menu.values()])
    
    prompt = f"""
    You are a food order bot. The menu is: {menu_str}.
    Parse the user's input into a structured order (item names and quantities).
    User input: "{user_input}"
    Respond in JSON format: 
    - For valid orders: [{{"item": "item_name", "quantity": number}}, ...]
    - For invalid orders: {{"error": "message"}}
    Match item names exactly as they appear in the menu (case-insensitive).
    If no quantity is specified, assume 1.
    """
    
    model = "mistral-large-latest"
        
 

    try:
       
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
            return None, result["error"]
        
        messages = []
        for order_item in result:
            item_name = order_item["item"]
            qty = order_item["quantity"]
            
            for item_id, item in menu.items():
                if item["name"].lower() == item_name.lower():
                    order[item_id] = qty
                    messages.append(f"Added {qty} x {item['name']} to your order.")
                    break
            else:
                messages.append(f"Sorry, '{item_name}' is not on the menu.")
        
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
def process_order(order, details, menu):
    if not order:
        print("\nNo items in your order. Goodbye!")
        return
    
    print("\n=== Order Summary ===")
    total = 0
    for item_id, qty in order.items():
        item = menu[item_id]
        cost = item["price"] * qty
        total += cost
        print(f"{item['name']} x{qty} - ₹{cost}")
    print(f"Total: ₹{total}")
    print(f"Delivery to: {details['name']}, {details['address']}, {details['phone']}")
    print("=====================\n")
    
    print("Processing your order...")
    time.sleep(2)
    print("Order placed successfully! You'll receive a confirmation soon.")

# Main function to run the bot
def main():
    print("Welcome to the Zomato Order Bot!")
    print("Loading menu and user data from APIs...\n")
    
    # Fetch menu using tool call
    menu = fetch_menu_from_api()
    if not menu:
        print("Unable to proceed without a menu. Exiting.")
        return
    
    display_menu(menu)
    order = {}
    
    # Take order via natural language input
    while True:
        user_input = input("What would you like to order? (or 'done' to finish): ").strip()
        if user_input.lower() == "done":
            break
        
        new_order, message = parse_order_input(user_input, menu)
        print(message)
        if new_order:
            for item_id, qty in new_order.items():
                if item_id in order:
                    order[item_id] += qty  # Add to existing quantity
                else:
                    order[item_id] = qty
    
    # Fetch delivery details and process order
    if order:
        details = get_delivery_details()
        if details:
            process_order(order, details, menu)
        else:
            print("Cannot process order without delivery details.")
    else:
        print("No order to process. Thanks for visiting!")

if __name__ == "__main__":
    main()