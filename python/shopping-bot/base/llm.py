from mistralai import Mistral
import json
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
from config import config
from typing import Dict, Optional, List, Any

logger = logging.getLogger(__name__)

if not config.MISTRAL_API_KEY:
    logger.error("MISTRAL_API_KEY not set in environment")
    raise EnvironmentError("MISTRAL_API_KEY environment variable is required")
client = Mistral(api_key=config.MISTRAL_API_KEY)
logger.info("Mistral API client initialized successfully")

# Define tools (API functions) the LLM can call
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "login",
            "description": "Log in a user with username and password",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "The user's username"},
                    "password": {"type": "string", "description": "The user's password"}
                },
                "required": ["username", "password"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_restaurants",
            "description": "List all open restaurants",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "show_menu",
            "description": "Show the menu of available items",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_order",
            "description": "Add an item to the order",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {"type": "string", "description": "Name of the item to add"},
                    "quantity": {"type": "integer", "description": "Number of items to add", "default": 1}
                },
                "required": ["item_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_from_order",
            "description": "Remove an item from the order",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {"type": "string", "description": "Name of the item to remove"}
                },
                "required": ["item_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "show_order",
            "description": "Display the current order",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "review_order",
            "description": "Review the order before confirmation",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_order",
            "description": "Confirm and place the order",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancel the current order",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(Exception))
async def process_with_tools(user_input: str, session_data: Dict, tools: List[Dict] = TOOLS) -> tuple[str, Optional[List[Any]]]:
    """Process user input with tool calls using Mistral API."""
    logger.info(f"Processing input with tools: {user_input}")
    messages = [
        {"role": "system", "content": "You are a food order bot. Use the provided tools to handle user queries. Respond naturally and call tools as needed."},
        {"role": "user", "content": user_input}
    ]
    
    # Include session context in the prompt
    session_context = f"Session data: user_id={session_data.get('user_id', 'None')}, order={session_data.get('order', {})}, selected_restaurant={session_data.get('selected_restaurant', 'None')}"
    messages.append({"role": "system", "content": session_context})

    try:
        response = await client.chat(
            model="mistral-large-latest",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        message = response.choices[0].message
        content = message.content.strip()
        tool_calls = message.tool_calls if hasattr(message, "tool_calls") else None
        
        logger.debug(f"LLM response: content='{content}', tool_calls={tool_calls}")
        return content, tool_calls
    except Exception as e:
        logger.error(f"Error in LLM processing: {str(e)}")
        return "Sorry, I couldn't process your request due to an internal error. Please try again.", None