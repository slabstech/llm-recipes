import gradio as gr
import uuid
from order_logic import fetch_menu_from_api, process_order

# Chat function for Gradio with session ID and login credentials
def chat_function(user_input, history, session_id, username, password):
    if history is None:
        history = []

    # Process user input using order logic with session ID and credentials
    response = process_order(session_id, user_input, username, password)
    history.append([user_input, response])
    return history, "", username, password


# Initial load function to display greeting and generate session ID
def load_greeting():
    session_id = str(uuid.uuid4())
    error, loaded_restaurants = fetch_menu_from_api()
    initial_message = (
        "Welcome to the Food Order Bot! Please log in first (e.g., 'login user1 password123').\n"
        "After logging in, you can order (e.g., 'I want 2 butter chickens'), 'show order', 'remove [item]', or 'done'."
    )
    if error:
        return [[None, error]], session_id, "", ""
    return [[None, initial_message]], session_id, "", ""


# Gradio interface setup
with gr.Blocks(title="Food Order Bot") as demo:
    # State variables
    session_id_state = gr.State()
    username_state = gr.State(value="")
    password_state = gr.State(value="")

    # Chatbot component
    chatbot = gr.Chatbot(label="Chat with Food Order Bot", height=600, scale=1)
    chat_input = gr.Textbox(
        placeholder="Type 'login username password', your order, 'done', 'show order', or 'remove [item]'",
        label="Your Order",
    )

    # Custom CSS for resizable chat area
    gr.Markdown(
        """
    <style>
        .chatbot-container { 
            resize: vertical; 
            overflow: auto; 
            min-height: 300px; 
            max-height: 80vh; 
        }
    </style>
    """
    )

    # Load initial greeting and session ID on start
    demo.load(
        load_greeting,
        outputs=[chatbot, session_id_state, username_state, password_state],
    )

    # Submit handler
    chat_input.submit(
        chat_function,
        inputs=[chat_input, chatbot, session_id_state, username_state, password_state],
        outputs=[chatbot, chat_input, username_state, password_state],
    )

demo.launch()
