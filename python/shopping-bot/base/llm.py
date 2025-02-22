from mistralai import Mistral
import json
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
from config import config
from typing import Dict, Optional, List, Any
import asyncio

logger = logging.getLogger(__name__)

if not config.MISTRAL_API_KEY:
    logger.error("MISTRAL_API_KEY not set in environment")
    raise EnvironmentError("MISTRAL_API_KEY environment variable is required")
client = Mistral(api_key=config.MISTRAL_API_KEY)  # Standard client
logger.info("Mistral API client initialized successfully")

# Define tools (unchanged)
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
    """Process user input with tool calls using Mistral API (synchronous call wrapped in async)."""
    logger.info(f"Processing input with tools: {user_input}")
    messages = [
        {"role": "system", "content": "You are a food order bot. Use the provided tools to handle user queries. Respond naturally and call tools as needed."},
        {"role": "user", "content": user_input}
    ]
    
    # Include session context in the prompt
    session_context = f"Session data: user_id={session_data.get('user_id', 'None')}, order={session_data.get('order', {})}, selected_restaurant={session_data.get('selected_restaurant', 'None')}"
    messages.append({"role": "system", "content": session_context})

    try:
        # Since client.chat.complete is synchronous, wrap it in an async context
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        ))
        message = response.choices[0].message
        content = message.content.strip()
        tool_calls = message.tool_calls if hasattr(message, "tool_calls") and message.tool_calls else None
        
        logger.debug(f"LLM response: content='{content}', tool_calls={tool_calls}")
        return content, tool_calls
    except Exception as e:
        logger.error(f"Error in LLM processing: {str(e)}")
        return f"Sorry, I couldn’t process your request due to an internal error: {str(e)}. Please try again.", None

# Legacy synchronous function (kept for compatibility with existing calls)
def parse_and_search_order(user_input: str, restaurants: Dict, selected_restaurant: Optional[str] = None) -> tuple[str, Dict]:
    """Fallback synchronous parsing for add_to_order (to be phased out)."""
    logger.warning("Using legacy parse_and_search_order; consider updating to tool-based approach")
    all_items = []
    item_map = {}
    for rest_id, rest_data in restaurants.items():
        for category, items in rest_data["menu"].items():
            for item in items:
                item_name = item["name"]
                all_items.append(f"{item_name} (from {rest_data['name']})")
                item_map[item_name.lower()] = {
                    "rest_id": rest_id,
                    "category": category,
                    "item_id": item["id"]
                }
    menu_str = ", ".join(all_items)
    
    prompt = f"""
    Parse the user's input into a structured order (item names and quantities).
    User input: "{user_input}"
    Available menu items: {menu_str}.
    Respond in JSON format:
    - For valid orders: [{{"item": "item_name", "quantity": number}}, ...]
    - For invalid orders: {{"error": "message"}}
    Match item names exactly (case-insensitive). If no quantity is specified, assume 1.
    """
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    response_content = response.choices[0].message.content.strip()
    
    try:
        result = json.loads(response_content)
        if "error" in result:
            return f"Sorry, I couldn't understand your order: {result['error']}. Please try rephrasing it (e.g., '2 Butter Idlis').", {}
        
        order = {}
        feedback = []
        for order_item in result:
            item_name = order_item["item"]
            qty = order_item["quantity"]
            item_key = item_name.lower()
            if item_key in item_map:
                details = item_map[item_key]
                rest_id = details["rest_id"]
                if selected_restaurant and rest_id != selected_restaurant:
                    feedback.append(f"Sorry, '{item_name}' is from {restaurants[rest_id]['name']}. You can only order from {restaurants[selected_restaurant]['name']}.")
                    continue
                category = details["category"]
                item_id = details["item_id"]
                order_key = f"{rest_id}:{category}:{item_id}"
                order[order_key] = qty
                feedback.append(f"Added {qty} x {item_name} (from {restaurants[rest_id]['name']}) to your order.")
            else:
                feedback.append(f"Sorry, '{item_name}' is not available on the menu. Please check the menu and try again.")
        return "\n".join(feedback), order
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM response as JSON: {str(e)} - Raw response: '{response_content}'")
        return "Sorry, I couldn’t process your order due to an issue with the response. Please try again.", {}