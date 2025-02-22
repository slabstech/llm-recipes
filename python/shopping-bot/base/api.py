import requests
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from datetime import datetime
import logging
from typing import Dict, Optional, List
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

BASE_URL = os.getenv("BASE_URL", "http://localhost:7861")
MENU_API_URL = f"{BASE_URL}/menu"
USERS_API_URL = f"{BASE_URL}/users/{{}}"
LOGIN_API_URL = f"{BASE_URL}/login"
ORDERS_API_URL = f"{BASE_URL}/orders"

def is_restaurant_open(opening_hours):
    now = datetime.now()
    current_time = now.hour * 60 + now.minute
    periods = opening_hours.split(", ")
    for period in periods:
        start_str, end_str = period.split(" – ")
        def parse_time(time_str):
            time_str = time_str.lower()
            is_pm = "pm" in time_str
            time_str = time_str.replace("am", "").replace("pm", "").replace("midnight", "0").replace("noon", "12")
            hour = int(time_str)
            if is_pm and hour != 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
            return hour * 60
        start_minutes = parse_time(start_str)
        end_minutes = parse_time(end_str)
        if end_minutes < start_minutes:
            end_minutes += 24 * 60
        if current_time >= start_minutes and (current_time <= end_minutes or current_time <= end_minutes - 24 * 60):
            return True
    return False

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def fetch_menu_from_api(token: str) -> tuple[Optional[str], Dict]:
    logger.info(f"Fetching menu from API: {MENU_API_URL} with token: {token}")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        logger.debug(f"Sending request with headers: {headers}")
        response = requests.get(MENU_API_URL, headers=headers, timeout=10, verify=False)  # Increased timeout
        response.raise_for_status()
        data = response.json()
        logger.debug(f"API response: {data}")
        if not data.get("success", False):
            raise ValueError("API response indicates failure")
        restaurants = data.get("restaurants", {})
        open_restaurants = {
            rest_id: rest_data for rest_id, rest_data in restaurants.items()
            if "opening_hours" in rest_data and is_restaurant_open(rest_data["opening_hours"])
        }
        return None, open_restaurants
    except requests.RequestException as e:
        logger.error(f"Failed to fetch menu from API: {str(e)} - Response: {e.response.text if e.response else 'No response'}")
        return str(e), {}
    except ValueError as e:
        logger.error(f"API returned invalid data: {str(e)}")
        return str(e), {}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def authenticate(username: str, password: str) -> Optional[str]:
    logger.info(f"Attempting to authenticate user: {username}")
    try:
        response = requests.post(
            LOGIN_API_URL,
            json={"username": username, "password": password},
            timeout=10,  # Increased timeout
            verify=False
        )
        response.raise_for_status()
        token = response.json().get("access_token")
        logger.info(f"Successfully authenticated user {username}. Token: {token}")
        return token
    except requests.RequestException as e:
        logger.error(f"Failed to authenticate user {username}: {str(e)}")
        return None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def fetch_user_credentials_from_api(user_id: str, token: str) -> tuple[Optional[str], Dict]:
    logger.info(f"Fetching user credentials for user_id: {user_id}")
    try:
        url = USERS_API_URL.format(user_id)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers, timeout=10, verify=False)  # Increased timeout
        response.raise_for_status()
        logger.info(f"Successfully fetched user credentials for {user_id}")
        return None, response.json().get("data", {})
    except requests.RequestException as e:
        logger.error(f"Failed to fetch user credentials: {str(e)}")
        return str(e), {}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def submit_order(order: Dict, token: str) -> tuple[Optional[str], Dict]:
    try:
        headers = {"Authorization": f"Bearer {token}"}
        order_items = [
            {"item_id": key.split(":")[2], "quantity": qty, "restaurant_id": key.split(":")[0], "category": key.split(":")[1]}
            for key, qty in order.items()
        ]
        response = requests.post(ORDERS_API_URL, json={"items": order_items}, headers=headers, timeout=10, verify=False)  # Increased timeout
        response.raise_for_status()
        return None, response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to submit order: {str(e)}")
        return str(e), {}