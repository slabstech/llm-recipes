from mistralai import Mistral
import json
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
import re
from typing import Dict, Optional, List
from logging_config import setup_logging  # Import shared config

logger = setup_logging(__name__)

try:
    MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=MISTRAL_API_KEY)
    logger.info("Mistral API client initialized successfully")
except KeyError as e:
    logger.error("MISTRAL_API_KEY environment variable not set")
    raise EnvironmentError("MISTRAL_API_KEY environment variable is required") from e
except Exception as e:
    logger.error(f"Failed to initialize Mistral client: {str(e)}")
    raise

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(Exception))
def parse_and_search_order(user_input: str, restaurants: Dict, selected_restaurant: Optional[str] = None) -> tuple[str, Dict]:
    logger.info(f"Parsing order input: {user_input} with selected restaurant: {selected_restaurant}")
    try:
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
        You are a food order bot. The menu items available are: {menu_str}.
        Parse the user's input into a structured order (item names and quantities).
        User input: "{user_input}"
        Respond in JSON format:
        - For valid orders: [{{"item": "item_name", "quantity": number}}, ...]
        - For invalid orders: {{"error": "message"}}
        Match item names exactly (case-insensitive). If no quantity is specified, assume 1.
        Ensure your response is valid JSON.
        """
        logger.debug(f"Sending prompt to Mistral API: {prompt}")
        
        chat_response = client.chat.complete(model="mistral-large-latest", messages=[{"role": "user", "content": prompt}])
        response_content = chat_response.choices[0].message.content.strip()
        logger.debug(f"Mistral API raw response: '{response_content}'")
        
        if not response_content:
            raise ValueError("Mistral API returned an empty response")
        
        try:
            result = json.loads(response_content)
        except json.JSONDecodeError:
            json_match = re.search(r'(\[.*\]|\{.*\})', response_content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
            else:
                raise
        
        if "error" in result:
            logger.warning(f"Order parsing failed: {result['error']}")
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
        logger.info(f"Successfully parsed order: {order}")
        return "\n".join(feedback), order
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Mistral API response as JSON: {str(e)} - Raw response: '{response_content}'")
        return "Sorry, I couldn't process your order due to an issue with the response. Please try rephrasing it or try again later.", {}
    except ValueError as e:
        logger.error(f"Mistral API error: {str(e)} - Raw response: '{response_content}'")
        return "Oops, something went wrong while understanding your order. Please try again or simplify your request (e.g., '1 Butter Idli').", {}
    except Exception as e:
        logger.error(f"Unexpected error in parse_and_search_order: {str(e)}")
        return "Something unexpected happened while processing your order. Please try again or contact support if this persists.", {}