import gradio as gr
from order_logic import fetch_menu_from_api, process_order

# Chat function for Gradio
def chat_function(user_input, history, order, restaurants, awaiting_confirmation):
    if history is None:
        history = []
    
    # Process user input using order logic
    response, new_order, new_awaiting = process_order(user_input, order, restaurants, awaiting_confirmation)
    history.append([user_input, response])
    return history, new_order, restaurants, new_awaiting, ""

# Initial load function to display greeting
def load_greeting():
    error, loaded_restaurants = fetch_menu_from_api()
    initial_message = ("Welcome to the Food Order Bot! What would you like to order? "
                      "(e.g., 'I want 2 butter chickens and a veg pizza')\n"
                      "You can also type 'show order' to see your current order or 'remove [item]' to remove an item.")
    if error:
        return [[None, error]], {}, loaded_restaurants, False
    return [[None, initial_message]], {}, loaded_restaurants, False

# Gradio interface setup
with gr.Blocks(title="Food Order Bot") as demo:
    # State variables
    order_state = gr.State(value={})
    restaurants_state = gr.State(value={})
    awaiting_confirmation_state = gr.State(value=False)
    
    # Chatbot component
    chatbot = gr.Chatbot(
        label="Chat with Food Order Bot",
        height=600,  # Larger initial height
        scale=1      # Allow scaling with window
    )
    chat_input = gr.Textbox(
        placeholder="Type your order here, 'done' to finish, 'show order', or 'remove [item]'",
        label="Your Order"
    )
    
    # Custom CSS for resizable chat area
    gr.Markdown("""
    <style>
        .chatbot-container { 
            resize: vertical; 
            overflow: auto; 
            min-height: 300px; 
            max-height: 80vh; 
        }
    </style>
    """)
    
    # Load initial greeting on start
    demo.load(
        load_greeting,
        outputs=[chatbot, order_state, restaurants_state, awaiting_confirmation_state]
    )
    
    # Submit handler
    chat_input.submit(
        chat_function,
        inputs=[chat_input, chatbot, order_state, restaurants_state, awaiting_confirmation_state],
        outputs=[chatbot, order_state, restaurants_state, awaiting_confirmation_state, chat_input]
    )

demo.launch()