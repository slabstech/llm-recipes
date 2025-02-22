import gradio as gr
import uuid
import speech_recognition as sr
from agent_order_logic import fetch_menu_from_api, process_order  # Correct import
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("food_order_bot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to convert audio to text
def audio_to_text(audio_file):
    if not audio_file or not isinstance(audio_file, str):
        logger.error("Invalid audio file")
        return "Failed to process audio. Please ensure your microphone is working."

    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            logger.info(f"Recognized speech: {text}")
            return text
    except sr.UnknownValueError:
        logger.warning("Could not understand audio")
        return "Sorry, I couldn't understand your voice command."
    except sr.RequestError as e:
        logger.error(f"Speech recognition error: {str(e)}")
        return f"Speech recognition failed: {str(e)}."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"An error occurred: {str(e)}."


# Chat function
def chat_function(user_input, history, session_id, username, password):
    if history is None:
        history = []
    response = process_order(session_id, user_input, username, password)
    history.append([user_input, response])
    return history, "", username, password


# Voice function
def voice_function(audio_file, history, session_id, username, password):
    if history is None:
        history = []
    text = audio_to_text(audio_file)
    if "error" in text.lower() or text.startswith("Sorry") or text.startswith("Failed"):
        history.append([None, text])
        return history, username, password
    response = process_order(session_id, text, username, password)
    history.append([text, response])
    return history, username, password


# Initial load function
def load_greeting():
    session_id = str(uuid.uuid4())
    error, restaurants = fetch_menu_from_api()
    initial_message = (
        "Welcome to the Food Order Bot!\n"
        "1. Log in: 'login <username> <password>' (e.g., 'login user1 password123').\n"
        "2. List open restaurants: 'list restaurants'.\n"
        "3. Order by speaking or typing (e.g., '2 Butter Idlis'). Orders are restricted to one restaurant after the first item.\n"
        "4. Manage: 'show order', 'remove [item]', 'done'."
    )
    if error or not restaurants:
        return (
            [[None, initial_message + "\n\nNo restaurants are currently open."]],
            session_id,
            "",
            "",
        )
    open_list = "\n".join(
        [
            f"- {data['name']} ({', '.join(data['cuisine'])})"
            for data in restaurants.values()
        ]
    )
    return (
        [[None, initial_message + f"\n\nOpen restaurants:\n{open_list}"]],
        session_id,
        "",
        "",
    )


# Gradio interface
with gr.Blocks(title="Food Order Bot") as demo:
    session_id_state = gr.State()
    username_state = gr.State(value="")
    password_state = gr.State(value="")

    chatbot = gr.Chatbot(label="Chat with Food Order Bot", height=600, scale=1)
    voice_input = gr.Audio(label="Speak Your Order", type="filepath")
    chat_input = gr.Textbox(
        placeholder="Type 'login username password', 'list restaurants', order, 'done', 'show order', or 'remove [item]'",
        label="Your Order",
    )

    gr.Markdown(
        """
    <style>
        .chatbot-container { resize: vertical; overflow: auto; min-height: 300px; max-height: 80vh; }
    </style>
    """
    )

    demo.load(
        load_greeting,
        outputs=[chatbot, session_id_state, username_state, password_state],
    )

    chat_input.submit(
        chat_function,
        inputs=[chat_input, chatbot, session_id_state, username_state, password_state],
        outputs=[chatbot, chat_input, username_state, password_state],
    )
    voice_input.change(
        voice_function,
        inputs=[voice_input, chatbot, session_id_state, username_state, password_state],
        outputs=[chatbot, username_state, password_state],
    )

demo.launch()
