import requests
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

BASE_URL = os.getenv("BASE_URL", "http://localhost:7861")
MENU_API_URL = f"{BASE_URL}/menu"
USERS_API_URL = f"{BASE_URL}/users/{{}}"
LOGIN_API_URL = f"{BASE_URL}/login"
ORDERS_API_URL = f"{BASE_URL}/orders"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def fetch_menu_from_api(token=None):
    logger.info(f"Fetching menu from API: {MENU_API_URL} with token: {token}")
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        logger.debug(f"Sending request with headers: {headers}")
        response = requests.get(MENU_API_URL, headers=headers, timeout=5, verify=False)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"API response: {data}")
        if not data.get("success", False):
            raise ValueError("API response indicates failure")
        restaurants = data.get("restaurants", {})
        return None, restaurants
    except requests.RequestException as e:
        logger.error(f"Failed to fetch menu from API: {str(e)} - Response: {e.response.text if e.response else 'No response'}")
        return str(e), {}
    except ValueError as e:
        logger.error(f"API returned invalid data: {str(e)}")
        return str(e), {}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def authenticate(username, password):
    logger.info(f"Attempting to authenticate user: {username}")
    try:
        response = requests.post(
            LOGIN_API_URL,
            json={"username": username, "password": password},
            timeout=5,
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
def fetch_user_credentials_from_api(user_id, token):
    logger.info(f"Fetching user credentials for user_id: {user_id}")
    try:
        url = USERS_API_URL.format(user_id)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        response.raise_for_status()
        logger.info(f"Successfully fetched user credentials for {user_id}")
        return None, response.json().get("data", {})
    except requests.RequestException as e:
        logger.error(f"Failed to fetch user credentials: {str(e)}")
        return str(e), {}

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def submit_order(order, token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        order_items = [
            {"item_id": key.split(":")[2], "quantity": qty, "restaurant_id": key.split(":")[0], "category": key.split(":")[1]}
            for key, qty in order.items()
        ]
        response = requests.post(ORDERS_API_URL, json={"items": order_items}, headers=headers, timeout=5, verify=False)
        response.raise_for_status()
        return None, response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to submit order: {str(e)}")
        return str(e), {}