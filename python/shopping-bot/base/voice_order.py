import gradio as gr
import uuid
import speech_recognition as sr
from order_logic import fetch_menu_from_api, process_order
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("food_order_bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to convert audio to text
def audio_to_text(audio_file):
    if not audio_file or not isinstance(audio_file, str):
        logger.error("Invalid audio file: must be a valid filename string")
        return "Failed to process audio. Please ensure your microphone is working and try again."
    
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)  # Using Google Speech-to-Text (free tier)
            logger.info(f"Recognized speech: {text}")
            return text
    except sr.UnknownValueError:
        logger.warning("Could not understand audio")
        return "Sorry, I couldn't understand your voice command. Please speak clearly and try again."
    except sr.RequestError as e:
        logger.error(f"Speech recognition error: {str(e)}")
        return f"Speech recognition failed: {str(e)}. Please check your internet connection."
    except Exception as e:
        logger.error(f"Unexpected error in audio processing: {str(e)}")
        return f"An error occurred: {str(e)}. Please try again."

# Chat function for Gradio with session ID and login credentials (for text input)
def chat_function(user_input, history, session_id, username, password):
    if history is None:
        history = []
    
    # Process user input using order logic with session ID and credentials
    response = process_order(session_id, user_input, username, password)
    history.append([user_input, response])
    return history, "", username, password

# Voice function for Gradio with session ID and login credentials
def voice_function(audio_file, history, session_id, username, password):
    if history is None:
        history = []
    
    text = audio_to_text(audio_file)
    if text.startswith("Sorry") or text.startswith("Failed") or "error" in text.lower():
        history.append([None, text])
        return history, username, password
    
    response = process_order(session_id, text, username, password)
    history.append([text, response])
    return history, username, password

# Initial load function to display greeting and generate session ID
def load_greeting():
    session_id = str(uuid.uuid4())
    error, loaded_restaurants = fetch_menu_from_api()
    initial_message = ("Welcome to the Food Order Bot!\n"
                      "1. Log in by typing 'login <username> <password>' (e.g., 'login user1 password123') or use the voice input.\n"
                      "2. Type 'list restaurants' to see open restaurants.\n"
                      "3. Speak or type your order (e.g., 'I want 2 Butter Idlis'). Note: After your first item, you'll only order from that restaurant.\n"
                      "4. Use 'show order', 'remove [item]', or 'done' to manage your order.")
    if error:
        return [[None, initial_message + f"\n\nError: {error}"]], session_id, "", ""
    if not loaded_restaurants:
        return [[None, initial_message + "\n\nNo restaurants are currently open."]], session_id, "", ""
    open_list = "\n".join([f"- {data['name']} ({', '.join(data['cuisine'])})" for data in loaded_restaurants.values()])
    return [[None, initial_message + f"\n\nCurrently open restaurants:\n{open_list}"]], session_id, "", ""

# Gradio interface setup
with gr.Blocks(title="Food Order Bot") as demo:
    # State variables
    session_id_state = gr.State()
    username_state = gr.State(value="")
    password_state = gr.State(value="")
    
    # Chatbot component
    chatbot = gr.Chatbot(
        label="Chat with Food Order Bot",
        height=600,
        scale=1
    )
    # Voice input
    voice_input = gr.Audio(label="Speak Your Order", type="filepath")
    # Text input
    chat_input = gr.Textbox(
        placeholder="Type 'login username password', 'list restaurants', your order, 'done', 'show order', or 'remove [item]'",
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
        outputs=[chatbot, session_id_state, username_state, password_state]
    )
    
    # Submit handler for text input
    chat_input.submit(
        chat_function,
        inputs=[chat_input, chatbot, session_id_state, username_state, password_state],
        outputs=[chatbot, chat_input, username_state, password_state]
    )
    
    # Submit handler for voice input
    voice_input.change(
        voice_function,
        inputs=[voice_input, chatbot, session_id_state, username_state, password_state],
        outputs=[chatbot, username_state, password_state]
    )

demo.launch()