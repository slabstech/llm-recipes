import gradio as gr
import uuid
import speech_recognition as sr
from api import process_order, login
from logging_config import setup_logging
from typing import List, Tuple, Optional

logger = setup_logging(__name__)

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
        return f"I couldn't process your voice input due to a connection issue. Please check your internet and try again."
    except Exception as e:
        logger.error(f"Unexpected error in audio processing: {str(e)}")
        return "Oops! Something went wrong with voice recognition. Please try again or type your order instead."


def chat_function(
    user_input: str,
    history: Optional[List[Tuple[str, str]]],
    session_id: str,
    token: str,
    username: str,
    password: str,
) -> Tuple[List[Tuple[str, str]], str, str, str]:
    if history is None:
        history = []
    logger.debug(f"Processing chat input: {user_input}")
    if user_input.startswith("login ") and not token:
        parts = user_input.split(" ", 2)
        if len(parts) != 3:
            response = "Please provide both username and password (e.g., 'login user1 password123')."
        else:
            username, password = parts[1], parts[2]
            token = login(username, password)
            response = (
                process_order(session_id, user_input, token, username, password)
                if token
                else "Login failed. Please check your credentials."
            )
    else:
        response = process_order(session_id, user_input, token)
    # Split the response into lines and append each as a separate bot message
    response_lines = response.split("\n")
    for line in response_lines:
        if line.strip():  # Only add non-empty lines
            history.append(
                (user_input if line == response_lines[0] else None, line.strip())
            )
    return history, "", token, username


def voice_function(
    audio_file: str,
    history: Optional[List[Tuple[str, str]]],
    session_id: str,
    token: str,
    username: str,
    password: str,
) -> Tuple[List[Tuple[str, str]], str, str, str]:
    if history is None:
        history = []
    text = audio_to_text(audio_file)
    if text.startswith("Sorry") or text.startswith("Failed") or "error" in text.lower():
        response_lines = text.split("\n")
        for line in response_lines:
            if line.strip():
                history.append((None, line.strip()))
        return history, token, username, password
    logger.debug(f"Processing voice input: {text}")
    if text.startswith("login ") and not token:
        parts = text.split(" ", 2)
        if len(parts) != 3:
            response = "Please provide both username and password (e.g., 'login user1 password123')."
        else:
            username, password = parts[1], parts[2]
            token = login(username, password)
            response = (
                process_order(session_id, text, token, username, password)
                if token
                else "Login failed. Please check your credentials."
            )
    else:
        response = process_order(session_id, text, token)
    # Split the response into lines and append each as a separate bot message
    response_lines = response.split("\n")
    for line in response_lines:
        if line.strip():
            history.append((text if line == response_lines[0] else None, line.strip()))
    return history, token, username, password


def load_greeting() -> Tuple[List[Tuple[Optional[str], str]], str, str, str, str]:
    session_id = str(uuid.uuid4())
    initial_messages = [
        "Welcome to the Food Order Bot!",
        "1. Log in by typing 'login <username> <password>' (e.g., 'login user1 password123')",
        "2. After logging in, type 'list restaurants' or 'menu' to see options",
        "3. Order items (e.g., '1 Butter Idli') - limited to one restaurant after first item",
        "4. Type 'done' to review, then 'confirm' to place or 'cancel' to discard your order",
        "5. Use 'show order' or 'remove [item]' to manage your order",
    ]
    logger.info(f"Initialized new session: {session_id}")
    history = [(None, msg) for msg in initial_messages]
    return history, session_id, "", "", ""


with gr.Blocks(title="Food Order Bot") as demo:
    session_id_state = gr.State()
    token_state = gr.State(value="")
    username_state = gr.State(value="")
    password_state = gr.State(value="")

    chatbot = gr.Chatbot(label="Chat with Food Order Bot", height=600, scale=1)
    voice_input = gr.Audio(label="Speak Your Order", type="filepath")
    chat_input = gr.Textbox(
        placeholder="Type 'login username password', 'list restaurants', 'menu', your order, 'done', 'confirm', 'cancel', 'show order', or 'remove [item]'",
        label="Your Order",
    )

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

    demo.load(
        load_greeting,
        outputs=[
            chatbot,
            session_id_state,
            token_state,
            username_state,
            password_state,
        ],
    )

    chat_input.submit(
        chat_function,
        inputs=[
            chat_input,
            chatbot,
            session_id_state,
            token_state,
            username_state,
            password_state,
        ],
        outputs=[chatbot, chat_input, token_state, username_state],
    )

    voice_input.change(
        voice_function,
        inputs=[
            voice_input,
            chatbot,
            session_id_state,
            token_state,
            username_state,
            password_state,
        ],
        outputs=[chatbot, token_state, username_state, password_state],
    )

demo.launch()
