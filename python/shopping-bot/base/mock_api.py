from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Header,
    Request,
)  # Add Request import
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict
import uvicorn
import json
import os
from logging_config import setup_logging
from db import save_order, load_order, save_state, load_state
from order_processor import process_order
from config import config
from models import (
    LoginRequest,
    UserResponse,
    OrderRequest,
    OrderResponse,
    ProcessOrderRequest,
)
from typing import Dict, Optional, List
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
    "user1": {
        "name": "John Doe",
        "address": "123 Main St, Bangalore",
        "phone": "9876543210",
        "password": "password123",
    },
    "user2": {
        "name": "Jane Smith",
        "address": "456 Elm St, Bangalore",
        "phone": "1234567890",
        "password": "securepass456",
    },
}


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
        raise HTTPException(
            status_code=403, detail=f"Invalid or expired token: {str(e)}"
        )


@app.post("/login")
async def login(login_data: LoginRequest):
    username = login_data.username
    password = login_data.password
    if username in USERS and USERS[username]["password"] == password:
        token = jwt.encode(
            {"user_id": username, "exp": datetime.utcnow() + timedelta(hours=1)},
            config.SECRET_KEY,
            algorithm=config.ALGORITHM,
        )
        logger.info(f"Generated token for {username}: {token}")
        return {"access_token": token, "token_type": "bearer"}
    logger.error(f"Login failed for {username}")
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/menu")
async def get_menu(current_user: str = Depends(get_current_user)):
    logger.info(f"Fetching menu for user: {current_user}")
    return {"success": True, "restaurants": RESTAURANTS}


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
            "phone": user["phone"],
        },
    }


@app.post("/orders", response_model=OrderResponse)
async def create_order(
    order: OrderRequest, current_user: str = Depends(get_current_user)
):
    logger.info(f"Creating order for user: {current_user}")
    total = 0.0
    for item in order.items:
        rest_id = item.restaurant_id
        if rest_id not in RESTAURANTS:
            logger.error(f"Restaurant {rest_id} not found")
            raise HTTPException(
                status_code=400, detail=f"Restaurant {rest_id} not found"
            )
        restaurant = RESTAURANTS[rest_id]
        category = item.category
        if category not in restaurant["menu"]:
            logger.error(f"Category {category} not found in restaurant {rest_id}")
            raise HTTPException(
                status_code=400,
                detail=f"Category {category} not found in restaurant {rest_id}",
            )
        menu_item = next(
            (i for i in restaurant["menu"][category] if i["id"] == item.item_id), None
        )
        if not menu_item:
            logger.error(f"Item {item.item_id} not found in category {category}")
            raise HTTPException(
                status_code=400,
                detail=f"Item {item.item_id} not found in category {category}",
            )
        total += menu_item["price"] * item.quantity

    order_id = str(uuid.uuid4())
    items_list = [item.dict() for item in order.items]
    save_order(order_id, current_user, items_list, total)
    logger.info(f"Order {order_id} created and saved to database")
    return OrderResponse(
        order_id=order_id, items=order.items, total=total, status="Placed"
    )


@app.get("/orders/{order_id}")
async def get_order(order_id: str, current_user: str = Depends(get_current_user)):
    logger.info(f"Fetching order {order_id} for user: {current_user}")
    order_data = load_order(order_id)
    if not order_data:
        logger.warning(f"Order {order_id} not found")
        raise HTTPException(status_code=404, detail="Order not found")
    if order_data["user_id"] != current_user:
        logger.error(f"User {current_user} not authorized to access order {order_id}")
        raise HTTPException(
            status_code=403, detail="Not authorized to access this order"
        )
    return {"success": True, "data": order_data}


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
    current_user: str = Depends(get_current_user),
):
    logger.info(f"Searching restaurants for user: {current_user}")
    return {"success": True, "data": list(RESTAURANTS.values())}


@app.post("/process_order")
async def process_order_endpoint(
    request: ProcessOrderRequest,
    http_request: Request,
    current_user: Optional[str] = Depends(get_current_user, use_cache=False),
):
    logger.info(f"Processing order request for session {request.session_id}")
    token = None
    if current_user:
        authorization = http_request.headers.get("Authorization", "")
        if authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
    response = await process_order(
        request.session_id,
        request.user_input,
        request.username,
        request.password,
        token,
        RESTAURANTS,
    )
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7861)
