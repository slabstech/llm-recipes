from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import uvicorn
import json
import os
import uuid
import logging

app = FastAPI(title="Zomato API Mock")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Ensure this path is correct based on your fix
MENU_FILE = "restaurants.json"  # Adjust if you moved it, e.g., "./data/restaurants.json"

def load_menu_data() -> Dict:
    if not os.path.exists(MENU_FILE):
        logger.error(f"Menu file not found at {MENU_FILE}")
        return {}
    with open(MENU_FILE, "r") as f:
        data = json.load(f)
        return data.get("restaurants", {})

RESTAURANTS = load_menu_data()

USERS = {
    "user1": {"name": "John Doe", "address": "123 Main St, Bangalore", "phone": "9876543210", "password": "password123"},
    "user2": {"name": "Jane Smith", "address": "456 Elm St, Bangalore", "phone": "1234567890", "password": "securepass456"}
}

ORDERS: Dict[str, dict] = {}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

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

async def get_current_user(authorization: Optional[str] = Header(default=None, alias="Authorization")):
    if not authorization or not authorization.startswith("Bearer "):
        logger.error(f"Invalid API-Key format: {authorization}")
        raise HTTPException(status_code=403, detail="Invalid API-Key")
    token = authorization.split(" ")[1]
    logger.debug(f"Received token: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
        }, SECRET_KEY, algorithm=ALGORITHM)
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
    if user_id not in USERS:
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
    total = 0.0
    for item in order.items:
        rest_id = item.restaurant_id
        if rest_id not in RESTAURANTS:
            raise HTTPException(status_code=400, detail=f"Restaurant {rest_id} not found")
        restaurant = RESTAURANTS[rest_id]
        category = item.category
        if category not in restaurant["menu"]:
            raise HTTPException(status_code=400, detail=f"Category {category} not found in restaurant {rest_id}")
        menu_item = next((i for i in restaurant["menu"][category] if i["id"] == item.item_id), None)
        if not menu_item:
            raise HTTPException(status_code=400, detail=f"Item {item.item_id} not found in category {category}")
        total += menu_item["price"] * item.quantity
    
    order_id = str(uuid.uuid4())
    order_data = {
        "order_id": order_id,
        "items": [item.dict() for item in order.items],
        "total": total,
        "status": "Placed",
        "user_id": current_user
    }
    ORDERS[order_id] = order_data
    
    return OrderResponse(
        order_id=order_id,
        items=order.items,
        total=total,
        status="Placed"
    )

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
    return {
        "success": True,
        "data": list(RESTAURANTS.values())
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7861
    )