import gradio as gr
from order_logic import fetch_menu_from_api, fetch_user_credentials_from_api, generate_order_summary, is_single_restaurant, parse_and_search_order

# Chatbot logic
def chatbot_response(user_input, history, order, restaurants, awaiting_confirmation):
    if not restaurants:
        return "Failed to load restaurant data. Please try again later.", order, False
    
    user_input = user_input.strip().lower()
    
    # Handle order input
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

# Gradio chat interface
def load_initial_data():
    error, restaurants = fetch_menu_from_api()
    if error:
        return error, {}, {}
    return "Welcome to the Food Order Bot! What would you like to order? (e.g., 'I want 2 butter chickens and a veg pizza')", {}, restaurants

with gr.Blocks(title="Food Order Bot") as demo:
    order_state = gr.State(value={})
    restaurants_state = gr.State(value={})
    
    chatbot = gr.Chatbot()
    chat_input = gr.Textbox(placeholder="Type your order here or 'done' to finish", label="Chat with the bot")
    
    def chat_wrapper(user_input, history):
        if history is None:
            history = []
        initial_message, order, restaurants = load_initial_data()
        if not history:
            history.append(["", initial_message])
        
        response, new_order, awaiting = chatbot_response(user_input, history, order_state.value, restaurants_state.value, False)
        order_state.value = new_order
        restaurants_state.value = restaurants
        history.append([user_input, response])
        return history, ""  # Clear input box
    
    chat_input.submit(chat_wrapper, inputs=[chat_input, chatbot], outputs=[chatbot, chat_input])

demo.launch()