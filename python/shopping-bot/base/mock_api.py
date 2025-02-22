from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import uvicorn
import json
import os

app = FastAPI(title="Zomato API Mock")

# Data loading
MENU_FILE = "restaurants.json"

def load_menu_data() -> Dict:
    if not os.path.exists(MENU_FILE):
        return {"restaurants": []}
    with open(MENU_FILE, "r") as f:
        data = json.load(f)
        return data["restaurants"]

RESTAURANTS = load_menu_data()

USERS = {
    "user1": {"name": "John Doe", "address": "123 Main St, Bangalore", "phone": "9876543210", "password": "password123"},
    "user2": {"name": "Jane Smith", "address": "456 Elm St, Bangalore", "phone": "1234567890", "password": "securepass456"}
}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    name: str
    address: str
    phone: str

# Token authentication
async def get_current_user(user_key: Optional[str] = Header(default=None)):
    if not user_key or not user_key.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Invalid API-Key")
    token = user_key.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None or user_id not in USERS:
            raise HTTPException(status_code=403, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

# Login endpoint
@app.post("/login")
async def login(login_data: LoginRequest):
    username = login_data.username
    password = login_data.password
    
    if username in USERS and USERS[username]["password"] == password:
        token = jwt.encode({
            "user_id": username,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Categories endpoint
@app.get("/categories")
async def get_categories(current_user: str = Depends(get_current_user)):
    return {
        "success": True,
        "data": [
            {"category_id": 1, "category_name": "Dine-out"},
            {"category_id": 2, "category_name": "Delivery"}
        ]
    }

# Cities endpoint
@app.get("/cities")
async def get_cities(
    q: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    city_ids: Optional[str] = None,
    count: Optional[int] = None,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": [{
            "id": 280,
            "name": "New York City, NY",
            "country_id": 216,
            "country_name": "United States"
        }]
    }

# Collections endpoint
@app.get("/collections")
async def get_collections(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    city_id: Optional[str] = None,
    count: Optional[int] = None,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": [{
            "collection_id": 1,
            "title": "Trending this week",
            "url": "https://www.zomato.com/new-york-city/top-restaurants",
            "description": "The most popular restaurants in town this week"
        }]
    }

# Cuisines endpoint
@app.get("/cuisines")
async def get_cuisines(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    city_id: Optional[str] = None,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": [
            {"cuisine_id": 25, "cuisine_name": "Chinese"},
            {"cuisine_id": 1, "cuisine_name": "American"}
        ]
    }

# Establishments endpoint
@app.get("/establishments")
async def get_establishments(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    city_id: Optional[str] = None,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": [
            {"establishment_id": 31, "establishment_name": "Bakery"},
            {"establishment_id": 1, "establishment_name": "Cafe"}
        ]
    }

# Geocode endpoint
@app.get("/geocode")
async def get_geocode(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": {
            "locality": {
                "entity_type": "group",
                "entity_id": 36932,
                "title": "Chelsea Market, Chelsea, New York City"
            },
            "popularity": {"popularity": 4.92}
        }
    }

# Locations endpoint
@app.get("/locations")
async def get_locations(
    query: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    count: Optional[int] = None,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": [{
            "entity_type": "city",
            "entity_id": 280,
            "title": "New York City"
        }]
    }

# Location details endpoint
@app.get("/location_details")
async def get_location_details(
    entity_id: int,
    entity_type: str,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "title": "Chelsea Market, Chelsea, New York City"
        }
    }

# Restaurant endpoint
@app.get("/restaurant")
async def get_restaurant(
    res_id: int,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": {
            "id": res_id,
            "name": "Sample Restaurant",
            "location": {"city": "New York City"}
        }
    }

# Daily menu endpoint
@app.get("/dailymenu")
async def get_daily_menu(
    res_id: int,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": {
            "daily_menu": {
                "daily_menu_id": 1,
                "name": "Daily Special",
                "dishes": [{"dish_id": 1, "name": "Special Dish", "price": "10$"}]
            }
        }
    }

# Reviews endpoint
@app.get("/reviews")
async def get_reviews(
    res_id: int,
    start: Optional[int] = None,
    count: Optional[int] = None,
    current_user: str = Depends(get_current_user)
):
    return {
        "success": True,
        "data": [{
            "rating": 4,
            "review_text": "Great food!",
            "user": {"name": "John Doe"}
        }]
    }

# Search endpoint
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
        "data": RESTAURANTS
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7861
    )