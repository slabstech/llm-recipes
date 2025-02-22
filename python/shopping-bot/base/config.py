import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class Config:
    """Centralized configuration loaded from .env."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    DB_FILE: str = os.getenv("DB_FILE", "zomato_orders.db")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:7861")
    MENU_FILE: str = os.getenv("MENU_FILE", "restaurants.json")
    MISTRAL_API_KEY: Optional[str] = os.getenv("MISTRAL_API_KEY")
    LOG_FILE: str = os.getenv("LOG_FILE", "food_order_bot.log")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    # Derived API URLs
    MENU_API_URL: str = f"{BASE_URL}/menu"
    USERS_API_URL: str = f"{BASE_URL}/users/{{}}"
    LOGIN_API_URL: str = f"{BASE_URL}/login"
    ORDERS_API_URL: str = f"{BASE_URL}/orders"


config = Config()
