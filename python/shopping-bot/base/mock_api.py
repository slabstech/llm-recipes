from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import uvicorn
import json
import os
import httpx  # Added missing import
from logging_config import setup_logging
from db import save_order, load_order, save_state, load_state
from llm import parse_and_search_order
from config import config
import bleach
import uuid
app = FastAPI(title="Zomato API Mock")
logger = setup_logging(__name__)

def load_menu_data() -> Dict:
    if not os.path.exists(config.MENU_FILE):
        logger.error(f"Menu file not found at {config.MENU_FILE}")
        raise FileNotFoundError(f"Menu file {config.MENU_FILE} not found")
    with open(config.MENU_FILE, "r") as f:
        logger.debug(f"Loading menu data from {config.MENU_FILE}")
        data = json.load(f)
        return data.get("restaurants", {})

try:
    RESTAURANTS = load_menu_data()
except FileNotFoundError as e:
    logger.critical(f"Failed to start server: {str(e)}")
    raise

USERS = {
    "user1": {"name": "John Doe", "address": "123 Main St, Bangalore", "phone": "9876543210", "password": "password123"},
    "user2": {"name": "Jane Smith", "address": "456 Elm St, Bangalore", "phone": "1234567890", "password": "securepass456"}
}

# Pydantic Models
class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    name: str
    address: str
    phone: str

class OrderItem(BaseModel):
    item_id: str
    quantity: int
    restaurant_id: str
    category: str

class OrderRequest(BaseModel):
    items: List[OrderItem]

class OrderResponse(BaseModel):
    order_id: str
    items: List[OrderItem]
    total: float
    status: str

class ProcessOrderRequest(BaseModel):
    session_id: str
    user_input: str
    username: Optional[str] = None
    password: Optional[str] = None

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        logger.error(f"Invalid API-Key format: {authorization}")
        raise HTTPException(status_code=403, detail="Invalid API-Key")
    token = authorization.split(" ")[1]
    logger.debug(f"Received token: {token}")
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        logger.debug(f"Decoded JWT payload: {payload}")
        user_id: str = payload.get("user_id")
        if user_id is None or user_id not in USERS:
            logger.error(f"Invalid token - user_id {user_id} not found")
            raise HTTPException(status_code=403, detail="Invalid token")
        return user_id
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)} - Token: {token}")
        raise HTTPException(status_code=403, detail=f"Invalid or expired token: {str(e)}")

@app.post("/login")
async def login(login_data: LoginRequest):
    username = login_data.username
    password = login_data.password
    if username in USERS and USERS[username]["password"] == password:
        token = jwt.encode({
            "user_id": username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, config.SECRET_KEY, algorithm=config.ALGORITHM)
        logger.info(f"Generated token for {username}: {token}")
        return {"access_token": token, "token_type": "bearer"}
    logger.error(f"Login failed for {username}")
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/menu")
async def get_menu(current_user: str = Depends(get_current_user)):
    logger.info(f"Fetching menu for user: {current_user}")
    return {
        "success": True,
        "restaurants": RESTAURANTS
    }

@app.get("/users/{user_id}")
async def get_user(user_id: str, current_user: str = Depends(get_current_user)):
    logger.debug(f"Fetching user details for {user_id} by {current_user}")
    if user_id not in USERS:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    user = USERS[user_id]
    return {
        "success": True,
        "data": {
            "name": user["name"],
            "address": user["address"],
            "phone": user["phone"]
        }
    }

@app.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderRequest, current_user: str = Depends(get_current_user)):
    logger.info(f"Creating order for user: {current_user}")
    total = 0.0
    for item in order.items:
        rest_id = item.restaurant_id
        if rest_id not in RESTAURANTS:
            logger.error(f"Restaurant {rest_id} not found")
            raise HTTPException(status_code=400, detail=f"Restaurant {rest_id} not found")
        restaurant = RESTAURANTS[rest_id]
        category = item.category
        if category not in restaurant["menu"]:
            logger.error(f"Category {category} not found in restaurant {rest_id}")
            raise HTTPException(status_code=400, detail=f"Category {category} not found in restaurant {rest_id}")
        menu_item = next((i for i in restaurant["menu"][category] if i["id"] == item.item_id), None)
        if not menu_item:
            logger.error(f"Item {item.item_id} not found in category {category}")
            raise HTTPException(status_code=400, detail=f"Item {item.item_id} not found in category {category}")
        total += menu_item["price"] * item.quantity
    
    order_id = str(uuid.uuid4())
    items_list = [item.dict() for item in order.items]
    save_order(order_id, current_user, items_list, total)
    logger.info(f"Order {order_id} created and saved to database")
    return OrderResponse(
        order_id=order_id,
        items=order.items,
        total=total,
        status="Placed"
    )

@app.get("/orders/{order_id}")
async def get_order(order_id: str, current_user: str = Depends(get_current_user)):
    logger.info(f"Fetching order {order_id} for user {current_user}")
    order_data = load_order(order_id)
    if not order_data:
        logger.warning(f"Order {order_id} not found")
        raise HTTPException(status_code=404, detail="Order not found")
    if order_data["user_id"] != current_user:
        logger.error(f"User {current_user} not authorized to access order {order_id}")
        raise HTTPException(status_code=403, detail="Not authorized to access this order")
    return {
        "success": True,
        "data": order_data
    }

@app.get("/search")
async def search_restaurants(
    entity_id: Optional[int] = None,
    entity_type: Optional[str] = None,
    q: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    start: Optional[int] = None,
    count: Optional[int] = None,
    cuisine: Optional[str] = None,
    radius: Optional[float] = None,
    establishment_type: Optional[str] = None,
    collection_id: Optional[str] = None,
    category: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    current_user: str = Depends(get_current_user)
):
    logger.info(f"Searching restaurants for user: {current_user}")
    return {
        "success": True,
        "data": list(RESTAURANTS.values())
    }

def generate_order_summary(order: Dict, restaurants: Dict) -> str:
    if not order:
        return "No items in your order."
    summary = ["=== Current Order ==="]
    total = 0.0
    for order_key, qty in order.items():
        rest_id, category, item_id = order_key.split(":")
        item = next(i for i in restaurants[rest_id]["menu"][category] if i["id"] == item_id)
        cost = item["price"] * qty
        total += cost
        summary.append(f"{item['name']} x{qty} (from {restaurants[rest_id]['name']}) - ${cost:.2f}")
    summary.append(f"Total: ${total:.2f}")
    return "\n".join(summary)

def remove_item_from_order(item_name: str, order: Dict, restaurants: Dict) -> str:
    item_name_lower = item_name.lower()
    for order_key, qty in list(order.items()):
        rest_id, category, item_id = order_key.split(":")
        item = next(i for i in restaurants[rest_id]["menu"][category] if i["id"] == item_id)
        if item["name"].lower() == item_name_lower:
            del order[order_key]
            logger.info(f"Removed item '{item_name}' from order")
            return f"Removed {item['name']} from your order."
    logger.warning(f"Item '{item_name}' not found in order")
    return f"'{item_name}' not found in your order."

def display_menu(restaurants: Dict) -> str:
    if not restaurants:
        return "No open restaurants available to display a menu."
    menu_lines = ["=== Available Menu ==="]
    for rest_id, rest_data in restaurants.items():
        menu_lines.append(f"\n{rest_data['name']} ({rest_data.get('opening_hours', 'Hours not specified')})")
        for category, items in rest_data["menu"].items():
            menu_lines.append(f"  {category}:")
            for item in items:
                menu_lines.append(f"    - {item['name']} (${item['price']:.2f})")
    menu_lines.append("\nType an order like '1 Butter Idli' or 'list restaurants' to continue.")
    logger.info(f"Displayed menu for {len(restaurants)} restaurants")
    return "\n".join(menu_lines)

@app.post("/process_order")
async def process_order_endpoint(request: ProcessOrderRequest):
    session_id = request.session_id
    user_input = request.user_input
    username = request.username
    password = request.password
    order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id = load_state(session_id)
    user_input = bleach.clean(user_input.strip().lower())
    
    try:
        if user_input.startswith("login "):
            parts = user_input.split(" ", 2)
            if len(parts) != 3:
                return "Please provide both username and password (e.g., 'login user1 password123')."
            username, password = parts[1], parts[2]
            token_response = await login(LoginRequest(username=username, password=password))
            token = token_response["access_token"]
            logger.debug(f"Token after login: {token}")
            async with httpx.AsyncClient() as client:
                response = await client.get(config.MENU_API_URL, headers={"Authorization": f"Bearer {token}"})
                if response.status_code != 200:
                    return f"Login succeeded, but I couldn't load the menu. Please try again later or contact support if this persists."
                data = response.json()
            restaurants = data.get("restaurants", {})
            user_id = username
            open_list = "\n".join([f"- {data['name']} ({data.get('opening_hours', 'Hours not specified')})" for data in restaurants.values()])
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
            logger.info(f"User {user_id} logged in successfully")
            return f"Logged in as {user_id}. Open restaurants:\n{open_list}\nWhat would you like to order?"
        
        if not user_id:
            return "Please log in first by typing 'login <username> <password>' (e.g., 'login user1 password123')."
        if not token:
            return "Please log in first by typing 'login <username> <password>' (e.g., 'login user1 password123')."
        
        if not restaurants:
            logger.debug(f"Fetching menu with existing token: {token}")
            async with httpx.AsyncClient() as client:
                response = await client.get(config.MENU_API_URL, headers={"Authorization": f"Bearer {token}"})
                if response.status_code != 200:
                    return "Sorry, I couldn't load the restaurant menu. Please try again later or log out and back in."
                data = response.json()
            restaurants = data.get("restaurants", {})
            if not restaurants:
                return "No restaurants are currently open. Please check back later!"
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
        
        if user_input == "list restaurants":
            open_list = "\n".join([f"- {data['name']} ({data.get('opening_hours', 'Hours not specified')})" for data in restaurants.values()])
            logger.info(f"Listed {len(restaurants)} open restaurants")
            return f"Currently open restaurants:\n{open_list}"
        
        if user_input == "menu":
            return display_menu(restaurants)
        
        if user_input == "show order":
            return generate_order_summary(order, restaurants)
        
        if user_input.startswith("remove "):
            item_name = user_input.replace("remove ", "").strip()
            if not item_name:
                return "Please specify an item to remove (e.g., 'remove Butter Idli')."
            feedback = remove_item_from_order(item_name, order, restaurants)
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
            return feedback
        
        if user_input == "done":
            if not order:
                return "You haven't added any items to your order yet. What would you like to order?"
            summary = generate_order_summary(order, restaurants)
            logger.info(f"Order review requested for session {session_id}")
            return f"{summary}\nPlease type 'confirm' to place your order or 'cancel' to discard it."
        
        if user_input == "confirm" and order:
            summary = generate_order_summary(order, restaurants)
            async with httpx.AsyncClient() as client:
                response = await client.get(config.USERS_API_URL.format(user_id), headers={"Authorization": f"Bearer {token}"})
                if response.status_code != 200:
                    return "I couldn't process your order because I can't retrieve your details. Please try again or log out and back in."
                credentials = response.json().get("data", {})
                order_request = OrderRequest(items=[
                    OrderItem(
                        item_id=key.split(":")[2],
                        quantity=qty,
                        restaurant_id=key.split(":")[0],
                        category=key.split(":")[1]
                    ) for key, qty in order.items()
                ])
                order_response = await client.post(config.ORDERS_API_URL, json=order_request.dict(), headers={"Authorization": f"Bearer {token}"})
                if order_response.status_code != 200:
                    return "Sorry, there was an issue placing your order. Please try again or contact support if this continues."
                order_data = order_response.json()
            name = credentials.get("name", "Unknown")
            address = credentials.get("address", "Unknown Address")
            phone = credentials.get("phone", "Unknown Phone")
            delivery_info = f"Delivery to: {name}, {address}, {phone}"
            response = f"{summary}\n{delivery_info}\n\nOrder placed successfully! Order ID: {order_data['order_id']}"
            save_state(session_id, {}, restaurants, False, user_id, token, None, order_data['order_id'])
            logger.info(f"Order confirmed for session {session_id}, Order ID: {order_data['order_id']}")
            return response
        elif user_input == "confirm" and not order:
            return "There's no order to confirm. Please add items to your order first (e.g., '1 Butter Idli')."
        
        if user_input == "cancel" and order:
            order.clear()
            save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, None, None)
            logger.info(f"Order cancelled for session {session_id}")
            return "Your order has been cancelled. What would you like to order next?"
        elif user_input == "cancel" and not order:
            return "There's no order to cancel."
        
        feedback, new_order = parse_and_search_order(user_input, restaurants, selected_restaurant)
        if new_order:
            if not selected_restaurant:
                selected_restaurant = list(new_order.keys())[0].split(":")[0]
            for order_key, qty in new_order.items():
                order[order_key] = order.get(order_key, 0) + qty
            logger.info(f"Added items to order for session {session_id}: {new_order}")
        save_state(session_id, order, restaurants, awaiting_confirmation, user_id, token, selected_restaurant, order_id)
        return f"{feedback}\n\nWhat else would you like to order from {restaurants[selected_restaurant]['name']}? (Type 'done' to review your order)"
    
    except Exception as e:
        logger.error(f"Unexpected error in order processing: {str(e)}")
        return "Oops! Something went wrong while processing your request. Please try again or contact support if this keeps happening."

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7861
    )