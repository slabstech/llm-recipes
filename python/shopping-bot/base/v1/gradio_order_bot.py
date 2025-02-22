import time
import requests
from mistralai import Mistral
import json
import os
import gradio as gr

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
        return None, data.get("restaurants", {})  # Return tuple: (error, restaurants)
    except requests.RequestException as e:
        return (
            f"Failed to fetch menu from API: {e}",
            {},
        )  # Return error message and empty dict


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

    model = "mistral-large-latest"

    try:
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
                        feedback.append(
                            f"Added {qty} x {item['name']} (from {rest_data['name']}) to your order."
                        )
                        found = True
                        break
                if found:
                    break
            if not found:
                feedback.append(
                    f"Sorry, '{item_name}' is not available at any restaurant."
                )

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


# Gradio interface functions
def add_to_order(user_input, current_order, restaurants):
    if not user_input.strip():
        return "Please enter an order.", current_order

    feedback, new_order = parse_and_search_order(user_input, restaurants)
    if new_order:
        for order_key, qty in new_order.items():
            if order_key in current_order:
                current_order[order_key] += qty
            else:
                current_order[order_key] = qty
    return feedback, current_order


def confirm_order(current_order, restaurants):
    if not current_order:
        return "No items to confirm.", False

    summary = generate_order_summary(current_order, restaurants)
    if is_single_restaurant(current_order):
        return f"{summary}\n\nReady to proceed with delivery details.", True
    else:
        return (
            f"{summary}\n\nYour order contains items from multiple restaurants. Typically, orders are from a single restaurant. Please confirm if you want to proceed.",
            False,
        )


def process_final_order(current_order, restaurants, confirm_multi_restaurant):
    if not current_order:
        return "No order to process.", False

    error, credentials = fetch_user_credentials_from_api()
    if error:
        return error, False

    name = credentials.get("name", "Unknown")
    address = credentials.get("address", "Unknown Address")
    phone = credentials.get("phone", "Unknown Phone")

    summary = generate_order_summary(current_order, restaurants)
    delivery_info = f"Delivery to: {name}, {address}, {phone}"

    if not is_single_restaurant(current_order) and not confirm_multi_restaurant:
        return (
            f"{summary}\n\nOrder not confirmed due to multiple restaurants. Please confirm to proceed.",
            False,
        )

    return (
        f"{summary}\n{delivery_info}\n\nProcessing your order...\nOrder placed successfully! You'll receive a confirmation soon.",
        True,
    )


# Gradio UI
with gr.Blocks(title="Food Order Bot") as demo:
    # State to store the order
    order_state = gr.State(value={})
    restaurants_state = gr.State(value={})

    # Welcome message
    gr.Markdown("## Welcome to the Food Order Bot!")

    # Step 1: Load restaurants and take order input
    with gr.Row():
        order_input = gr.Textbox(
            label="What would you like to order? (e.g., 'I want 2 butter chickens and a veg pizza')",
            placeholder="Enter your order here",
        )
        add_button = gr.Button("Add to Order")

    order_feedback = gr.Textbox(label="Order Feedback", interactive=False)

    # Step 2: Confirm order
    confirm_button = gr.Button("Confirm Order")
    confirm_output = gr.Textbox(label="Order Summary", interactive=False)
    multi_restaurant_confirmed = gr.Checkbox(
        label="Confirm order from multiple restaurants", visible=False
    )

    # Step 3: Finalize order
    process_button = gr.Button("Process Order")
    final_output = gr.Textbox(label="Final Confirmation", interactive=False)

    # Event handlers
    def load_restaurants():
        error, restaurants = fetch_menu_from_api()
        if error:
            return error, {}, "Failed to load restaurant data."
        return (
            "Restaurants loaded successfully.",
            restaurants,
            "Add items to your order.",
        )

    demo.load(
        load_restaurants, outputs=[order_feedback, restaurants_state, confirm_output]
    )

    add_button.click(
        add_to_order,
        inputs=[order_input, order_state, restaurants_state],
        outputs=[order_feedback, order_state],
    )

    confirm_button.click(
        confirm_order,
        inputs=[order_state, restaurants_state],
        outputs=[confirm_output, multi_restaurant_confirmed],
    )

    process_button.click(
        process_final_order,
        inputs=[order_state, restaurants_state, multi_restaurant_confirmed],
        outputs=[final_output, multi_restaurant_confirmed],
    )

demo.launch()
