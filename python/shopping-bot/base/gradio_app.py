import gradio as gr
import uuid
import speech_recognition as sr
from orders import process_order
import logging
from typing import List, Tuple, Optional

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("food_order_bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

recognizer = sr.Recognizer()

def audio_to_text(audio_file: str) -> str:
    if not audio_file or not isinstance(audio_file, str):
        logger.error("Invalid audio file: must be a valid filename string")
        return "Failed to process audio. Please ensure your microphone is working and try again."
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
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

def chat_function(user_input: str, history: Optional[List[Tuple[str, str]]], session_id: str, username: str, password: str) -> Tuple[List[Tuple[str, str]], str, str, str]:
    if history is None:
        history = []
    response = process_order(session_id, user_input, username, password)
    history.append((user_input, response))
    return history, "", username, password

def voice_function(audio_file: str, history: Optional[List[Tuple[str, str]]], session_id: str, username: str, password: str) -> Tuple[List[Tuple[str, str]], str, str]:
    if history is None:
        history = []
    text = audio_to_text(audio_file)
    if text.startswith("Sorry") or text.startswith("Failed") or "error" in text.lower():
        history.append((None, text))
        return history, username, password
    response = process_order(session_id, text, username, password)
    history.append((text, response))
    return history, username, password

def load_greeting() -> Tuple[List[Tuple[Optional[str], str]], str, str, str]:
    session_id = str(uuid.uuid4())
    initial_message = ("Welcome to the Food Order Bot!\n"
                      "1. Log in by typing 'login <username> <password>' (e.g., 'login user1 password123')\n"
                      "2. After logging in, type 'list restaurants' to see open restaurants\n"
                      "3. Order items (e.g., 'I want 2 Butter Idlis') - limited to one restaurant after first item\n"
                      "4. Use 'show order', 'remove [item]', or 'done' to manage your order")
    return [[None, initial_message]], session_id, "", ""

with gr.Blocks(title="Food Order Bot") as demo:
    session_id_state = gr.State()
    username_state = gr.State(value="")
    password_state = gr.State(value="")
    
    chatbot = gr.Chatbot(label="Chat with Food Order Bot", height=600, scale=1)
    voice_input = gr.Audio(label="Speak Your Order", type="filepath")
    chat_input = gr.Textbox(
        placeholder="Type 'login username password', 'list restaurants', your order, 'done', 'show order', or 'remove [item]'",
        label="Your Order"
    )
    
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
    
    demo.load(
        load_greeting,
        outputs=[chatbot, session_id_state, username_state, password_state]
    )
    
    chat_input.submit(
        chat_function,
        inputs=[chat_input, chatbot, session_id_state, username_state, password_state],
        outputs=[chatbot, chat_input, username_state, password_state]
    )
    
    voice_input.change(
        voice_function,
        inputs=[voice_input, chatbot, session_id_state, username_state, password_state],
        outputs=[chatbot, username_state, password_state]
    )

demo.launch()