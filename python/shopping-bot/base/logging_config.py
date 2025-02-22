import logging
from config import config  # Import config

def setup_logging(module_name: str) -> logging.Logger:
    """Configure logging with a level from environment variable LOG_LEVEL."""
    numeric_level = getattr(logging, config.LOG_LEVEL, logging.INFO)
    
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(module_name)