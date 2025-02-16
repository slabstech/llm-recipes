"""
This module contains utility functions and decorators used throughout the military decision agent system.
"""

import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that catches and logs any exceptions raised by the decorated function.
    
    Args:
        func (Callable): The function to be decorated.
    
    Returns:
        Callable: The decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper

def cache_result(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A simple caching decorator that stores the result of a function call.
    
    Args:
        func (Callable): The function to be decorated.
    
    Returns:
        Callable: The decorated function with caching.
    """
    cache = {}
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# Add more utility functions as needed
