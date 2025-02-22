import sqlite3
import json
import os
from logging_config import setup_logging
from config import config  # Import config
from typing import Dict, Optional, List

logger = setup_logging(__name__)

DB_FILE = config.DB_FILE  # Use config value


def init_db(force_reset=False):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if force_reset:
            logger.debug("Dropping existing tables")
            cursor.execute("DROP TABLE IF EXISTS sessions")
            cursor.execute("DROP TABLE IF EXISTS orders")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                order_data TEXT,
                restaurants TEXT,
                awaiting_confirmation INTEGER,
                user_id TEXT,
                token TEXT,
                selected_restaurant TEXT,
                order_id TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                user_id TEXT,
                items TEXT,
                total REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        logger.info("SQLite database initialized with sessions and orders tables")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    finally:
        conn.close()


def save_state(
    session_id,
    order,
    restaurants,
    awaiting_confirmation,
    user_id=None,
    token=None,
    selected_restaurant=None,
    order_id=None,
):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        logger.debug(f"Saving state for session {session_id} with order: {order}")
        cursor.execute(
            """
            INSERT OR REPLACE INTO sessions (session_id, order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                session_id,
                json.dumps(order),
                json.dumps(restaurants),
                int(awaiting_confirmation),
                user_id,
                token,
                selected_restaurant,
                order_id,
            ),
        )
        conn.commit()
        logger.info(f"Saved state for session {session_id} with token: {token}")
    except sqlite3.Error as e:
        logger.error(f"Failed to save state: {str(e)}")
        raise Exception(
            "Sorry, I couldn't save your session. Please try again or contact support."
        )
    finally:
        if conn:
            conn.close()


def load_state(session_id):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        logger.debug(f"Loading state for session {session_id}")
        cursor.execute(
            "SELECT order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id FROM sessions WHERE session_id = ?",
            (session_id,),
        )
        result = cursor.fetchone()
        if result:
            logger.debug(f"Loaded state for session {session_id}: {result}")
            return (
                json.loads(result[0]),
                json.loads(result[1]),
                bool(result[2]),
                result[3],
                result[4],
                result[5],
                result[6],
            )
        logger.info(f"No state found for session {session_id}")
        return {}, {}, False, None, None, None, None
    except sqlite3.Error as e:
        logger.error(f"Failed to load state: {str(e)}")
        raise Exception(
            "Sorry, I couldn't load your session. Please try restarting or contact support."
        )
    finally:
        if conn:
            conn.close()


def save_order(
    order_id: str, user_id: str, items: List[Dict], total: float, status: str = "Placed"
):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        logger.debug(f"Saving order {order_id} for user {user_id}")
        cursor.execute(
            """
            INSERT OR REPLACE INTO orders (order_id, user_id, items, total, status)
            VALUES (?, ?, ?, ?, ?)
        """,
            (order_id, user_id, json.dumps(items), total, status),
        )
        conn.commit()
        logger.info(f"Saved order {order_id} for user {user_id}")
    except sqlite3.Error as e:
        logger.error(f"Failed to save order: {str(e)}")
        raise Exception(
            "Sorry, I couldn't save your order. Please try again or contact support."
        )
    finally:
        if conn:
            conn.close()


def load_order(order_id: str) -> Optional[Dict]:
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        logger.debug(f"Loading order {order_id}")
        cursor.execute(
            "SELECT order_id, user_id, items, total, status, created_at FROM orders WHERE order_id = ?",
            (order_id,),
        )
        result = cursor.fetchone()
        if result:
            order_data = {
                "order_id": result[0],
                "user_id": result[1],
                "items": json.loads(result[2]),
                "total": result[3],
                "status": result[4],
                "created_at": result[5],
            }
            logger.debug(f"Loaded order {order_id}: {order_data}")
            return order_data
        logger.info(f"No order found for order_id {order_id}")
        return None
    except sqlite3.Error as e:
        logger.error(f"Failed to load order: {str(e)}")
        raise Exception(
            "Sorry, I couldn't load the order. Please try again or contact support."
        )
    finally:
        if conn:
            conn.close()


init_db(force_reset=False)
