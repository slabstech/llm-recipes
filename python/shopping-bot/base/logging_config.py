import logging
import os
from dotenv import load_dotenv

load_dotenv()

def setup_logging(module_name: str) -> logging.Logger:
    """Configure logging with a level from environment variable LOG_LEVEL."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level, logging.INFO)
    
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(os.getenv("LOG_FILE", "food_order_bot.log")),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(module_name)