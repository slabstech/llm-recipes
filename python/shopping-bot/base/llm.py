from mistralai import Mistral
import json
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "food_order_bot.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
def parse_and_search_order(user_input, restaurants, selected_restaurant=None):
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
        """
        logger.debug(f"Sending prompt to Mistral API: {prompt}")
        
        chat_response = client.chat.complete(model="mistral-large-latest", messages=[{"role": "user", "content": prompt}])
        response_content = chat_response.choices[0].message.content.strip()
        logger.debug(f"Mistral API raw response: '{response_content}'")
        
        if not response_content:
            raise ValueError("Mistral API returned an empty response")
        
        result = json.loads(response_content)
        
        if "error" in result:
            return result["error"], {}
        
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
                feedback.append(f"Sorry, '{item_name}' is not available.")
        
        return "\n".join(feedback), order
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Mistral API response as JSON: {str(e)} - Raw response: '{response_content}'")
        return f"Error parsing order: Invalid response from API - {str(e)}", {}
    except ValueError as e:
        logger.error(f"Mistral API error: {str(e)} - Raw response: '{response_content}'")
        return f"Error parsing order: {str(e)}", {}
    except Exception as e:
        logger.error(f"Unexpected error in parse_and_search_order: {str(e)}")
        return f"Error parsing order: {str(e)}", {}