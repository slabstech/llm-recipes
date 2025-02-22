import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from datetime import datetime
from logging_config import setup_logging
from config import config
from typing import Dict, Optional, Tuple, List

logger = setup_logging(__name__)

def login(username: str, password: str) -> Optional[str]:
    """Authenticate and return a token."""
    try:
        response = requests.post(
            config.LOGIN_API_URL,
            json={"username": username, "password": password},
            timeout=10,
            verify=False
        )
        response.raise_for_status()
        token = response.json().get("access_token")
        logger.info(f"Login successful for {username}")
        return token
    except requests.RequestException as e:
        logger.error(f"Login failed: {str(e)}")
        return None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
def process_order(session_id: str, user_input: str, token: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None) -> str:
    """Process user input via the FastAPI server."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    data = {
        "session_id": session_id,
        "user_input": user_input,
        "username": username,
        "password": password
    }
    try:
        response = requests.post(
            f"{config.BASE_URL}/process_order",
            json=data,
            headers=headers,
            timeout=10,
            verify=False
        )
        response.raise_for_status()
        logger.debug(f"Process order response: {response.text}")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to process order: {str(e)}")
        return "Sorry, I couldn't process your request. Please try again or check your connection."