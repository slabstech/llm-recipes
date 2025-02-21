import gradio as gr
import uuid
from order_logic import fetch_menu_from_api, process_order

# Chat function for Gradio with session ID
def chat_function(user_input, history, session_id):
    if history is None:
        history = []
    
    # Process user input using order logic with session ID
    response = process_order(session_id, user_input)
    history.append([user_input, response])
    return history, ""

# Initial load function to display greeting and generate session ID
def load_greeting():
    session_id = str(uuid.uuid4())  # Generate unique session ID
    error, loaded_restaurants = fetch_menu_from_api()
    initial_message = ("Welcome to the Food Order Bot! What would you like to order? "
                      "(e.g., 'I want 2 butter chickens and a veg pizza')\n"
                      "You can also type 'show order' to see your current order or 'remove [item]' to remove an item.")
    if error:
        return [[None, error]], session_id
    return [[None, initial_message]], session_id

# Gradio interface setup
with gr.Blocks(title="Food Order Bot") as demo:
    # State variable for session ID
    session_id_state = gr.State()
    
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
    
    # Load initial greeting and session ID on start
    demo.load(
        load_greeting,
        outputs=[chatbot, session_id_state]
    )
    
    # Submit handler
    chat_input.submit(
        chat_function,
        inputs=[chat_input, chatbot, session_id_state],
        outputs=[chatbot, chat_input]
    )

demo.launch()