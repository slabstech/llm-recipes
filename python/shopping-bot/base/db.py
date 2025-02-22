import sqlite3
import json
import os
from dotenv import load_dotenv
from logging_config import setup_logging  # Import shared config

logger = setup_logging(__name__)

DB_FILE = os.getenv("DB_FILE", "zomato_orders.db")

def init_db(force_reset=False):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if force_reset:
            logger.debug("Dropping existing sessions table")
            cursor.execute("DROP TABLE IF EXISTS sessions")
        cursor.execute("""
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
        """)
        conn.commit()
        logger.info("SQLite database initialized with updated schema")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    finally:
        conn.close()

def save_state(session_id, order, restaurants, awaiting_confirmation, user_id=None, token=None, selected_restaurant=None, order_id=None):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        logger.debug(f"Saving state for session {session_id} with order: {order}")
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (session_id, order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            json.dumps(order),
            json.dumps(restaurants),
            int(awaiting_confirmation),
            user_id,
            token,
            selected_restaurant,
            order_id
        ))
        conn.commit()
        logger.info(f"Saved state for session {session_id} with token: {token}")
    except sqlite3.Error as e:
        logger.error(f"Failed to save state: {str(e)}")
        raise Exception("Sorry, I couldn't save your session. Please try again or contact support.")
    finally:
        if conn:
            conn.close()

def load_state(session_id):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        logger.debug(f"Loading state for session {session_id}")
        cursor.execute("SELECT order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id FROM sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        if result:
            logger.debug(f"Loaded state for session {session_id}: {result}")
            return (json.loads(result[0]), json.loads(result[1]), bool(result[2]), result[3], result[4], result[5], result[6])
        logger.info(f"No state found for session {session_id}")
        return {}, {}, False, None, None, None, None
    except sqlite3.Error as e:
        logger.error(f"Failed to load state: {str(e)}")
        raise Exception("Sorry, I couldn't load your session. Please try restarting or contact support.")
    finally:
        if conn:
            conn.close()

init_db(force_reset=False)