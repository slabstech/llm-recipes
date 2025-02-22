from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
import uvicorn
import ssl

app = FastAPI(title="Restaurant API")

# Mock data (same as before)
RESTAURANTS = {
    "rest1": {"name": "Spice Haven", "menu": {"1": {"name": "Butter Chicken", "price": 250}, "2": {"name": "Paneer Tikka", "price": 200}}},
    "rest2": {"name": "Biryani Bliss", "menu": {"3": {"name": "Chicken Biryani", "price": 300}, "4": {"name": "Veg Biryani", "price": 220}}},
    "rest3": {"name": "Pizza Palace", "menu": {"5": {"name": "Veg Pizza", "price": 350}, "6": {"name": "Pepperoni Pizza", "price": 400}}}
}

USERS = {
    "user1": {"name": "John Doe", "address": "123 Main St, Delhi", "phone": "9876543210", "password": "password123"},
    "user2": {"name": "Jane Smith", "address": "456 Elm St, Mumbai", "phone": "1234567890", "password": "securepass456"}
}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Pydantic models for request validation
class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    name: str
    address: str
    phone: str

# Token dependency
async def get_current_user(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None or user_id not in USERS:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

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

# Menu endpoint
@app.get("/menu")
async def get_menu():
    return {"restaurants": RESTAURANTS}

# User endpoint with authentication
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: str = Depends(get_current_user)):
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    
    if user_id in USERS:
        user_data = {k: v for k, v in USERS[user_id].items() if k != "password"}
        return user_data
    raise HTTPException(status_code=404, detail="User not found")

# SSL configuration
#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#ssl_context.load_cert_chain('cert.pem', 'key.pem')

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7861,
#        ssl_keyfile="key.pem",
#        ssl_certfile="cert.pem"
    )