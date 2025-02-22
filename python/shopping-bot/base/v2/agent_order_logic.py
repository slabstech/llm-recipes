import time
import requests
from mistralai import Mistral
import json
import logging
import os
import sqlite3
import bleach
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from datetime import datetime
from crewai import Agent, Task, Crew

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "food_order_bot.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# SQLite setup
DB_FILE = os.getenv("DB_FILE", "zomato_orders.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            order_data TEXT,
            restaurants TEXT,
            awaiting_confirmation INTEGER,
            user_id TEXT,
            token TEXT,
            selected_restaurant TEXT
        )
    """)
    conn.commit()
    conn.close()
    logger.info("SQLite database initialized")

init_db()

# Mistral API client
try:
    MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=MISTRAL_API_KEY)
except KeyError as e:
    logger.error("MISTRAL_API_KEY environment variable not set")
    raise EnvironmentError("MISTRAL_API_KEY is required") from e

# API endpoints
MENU_API_URL = os.getenv("MENU_API_URL", "http://localhost:7861/menu")
USERS_API_URL = os.getenv("USERS_API_URL", "http://localhost:7861/users/{}")
LOGIN_API_URL = os.getenv("LOGIN_API_URL", "http://localhost:7861/login")

# Utility function to check if restaurant is open
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

# State management
def save_state(session_id, order, restaurants, awaiting_confirmation, user_id=None, token=None, selected_restaurant=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (session_id, order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, json.dumps(order), json.dumps(restaurants), int(awaiting_confirmation), user_id, token, selected_restaurant
        ))
        conn.commit()
        logger.info(f"Saved state for session {session_id}")
    except sqlite3.Error as e:
        logger.error(f"Failed to save state: {str(e)}")
    finally:
        conn.close()

def load_state(session_id):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT order_data, restaurants, awaiting_confirmation, user_id, token, selected_restaurant FROM sessions WHERE session_id = ?", (session_id,))
        result = cursor.fetchone()
        if result:
            return [json.loads(x) if isinstance(x, str) else x for x in result]
        logger.info(f"No state found for session {session_id}")
        return [{}, {}, False, None, None, None]
    except sqlite3.Error as e:
        logger.error(f"Failed to load state: {str(e)}")
        return [{}, {}, False, None, None, None]
    finally:
        conn.close()

# Define Agents with Mistral AI integration
def create_mistral_llm():
    return lambda prompt: client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

auth_agent = Agent(
    role="Authentication Agent",
    goal="Authenticate users and manage tokens",
    backstory="Specializes in secure user authentication.",
    verbose=True,
    allow_delegation=False,
    llm=create_mistral_llm()  # Custom Mistral LLM
)

menu_agent = Agent(
    role="Menu Agent",
    goal="Fetch and filter restaurant/menu data",
    backstory="Expert in retrieving and processing restaurant information.",
    verbose=True,
    allow_delegation=False,
    llm=create_mistral_llm()
)

order_parser_agent = Agent(
    role="Order Parser Agent",
    goal="Parse user input into structured orders",
    backstory="Uses AI to interpret natural language orders.",
    verbose=True,
    allow_delegation=False,
    llm=create_mistral_llm()
)

order_manager_agent = Agent(
    role="Order Manager Agent",
    goal="Manage the user's order (add, remove, summarize)",
    backstory="Keeps track of the order and ensures consistency.",
    verbose=True,
    allow_delegation=False,
    llm=create_mistral_llm()
)

feedback_agent = Agent(
    role="Feedback Agent",
    goal="Generate user-friendly responses",
    backstory="Crafts clear and helpful responses for users.",
    verbose=True,
    allow_delegation=False,
    llm=create_mistral_llm()
)

# Define Tasks
def auth_task(username, password):
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
    def authenticate():
        response = requests.post(LOGIN_API_URL, json={"username": username, "password": password}, timeout=5, verify=False)
        response.raise_for_status()
        return response.json().get("access_token")
    
    return Task(
        description=f"Authenticate user {username} with password {password}",
        agent=auth_agent,
        expected_output="Authentication token or error message",
        action=lambda: authenticate() if username and password else "Invalid credentials"
    )

def fetch_menu_task():
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_exception_type(requests.RequestException))
    def fetch():
        response = requests.get(MENU_API_URL, timeout=5, verify=False)
        response.raise_for_status()
        data = response.json()
        restaurants = data.get("restaurants", {})
        return {rest_id: rest_data for rest_id, rest_data in restaurants.items() if "opening_hours" in rest_data and is_restaurant_open(rest_data["opening_hours"])}
    
    return Task(
        description="Fetch and filter open restaurants",
        agent=menu_agent,
        expected_output="Dictionary of open restaurants",
        action=fetch
    )

def parse_order_task(user_input, restaurants, selected_restaurant):
    def parse():
        all_items = []
        item_map = {}
        for rest_id, rest_data in restaurants.items():
            for category, items in rest_data["menu"].items():
                for item in items:
                    item_name = item["name"]
                    all_items.append(f"{item_name} (from {rest_data['name']})")
                    item_map[item_name.lower()] = {"rest_id": rest_id, "category": category, "item_id": item["id"]}
        menu_str = ", ".join(all_items)
        
        prompt = f"""
        Parse the input into a structured order: "{user_input}"
        Menu items: {menu_str}
        Respond in JSON: [{{"item": "item_name", "quantity": number}}, ...] or {{"error": "message"}}
        Match items case-insensitively. Default quantity is 1.
        """
        response = client.chat.complete(model="mistral-large-latest", messages=[{"role": "user", "content": prompt}])
        result = json.loads(response.choices[0].message.content)
        
        if "error" in result:
            return result["error"], {}
        
        order = {}
        for order_item in result:
            item_name = order_item["item"].lower()
            qty = order_item["quantity"]
            if item_name in item_map:
                details = item_map[item_name]
                rest_id = details["rest_id"]
                if selected_restaurant and rest_id != selected_restaurant:
                    continue
                order[f"{rest_id}:{details['category']}:{details['item_id']}"] = qty
        return None, order
    
    return Task(
        description=f"Parse user input '{user_input}' into an order",
        agent=order_parser_agent,
        expected_output="Tuple of (feedback/error, order dict)",
        action=parse
    )

def manage_order_task(order, new_order, restaurants, action="add"):
    def manage():
        if action == "add":
            for key, qty in new_order.items():
                order[key] = order.get(key, 0) + qty
            return order
        elif action == "remove":
            item_name = new_order
            for order_key, qty in list(order.items()):
                rest_id, category, item_id = order_key.split(":")
                item = next(i for i in restaurants[rest_id]["menu"][category] if i["id"] == item_id)
                if item["name"].lower() == item_name.lower():
                    del order[order_key]
                    break
            return order
        elif action == "summary":
            if not order:
                return "No items in your order."
            summary = ["=== Current Order ==="]
            total = 0
            for key, qty in order.items():
                rest_id, category, item_id = key.split(":")
                item = next(i for i in restaurants[rest_id]["menu"][category] if i["id"] == item_id)
                cost = item["price"] * qty
                total += cost
                summary