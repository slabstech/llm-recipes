from pydantic import BaseModel
from typing import List

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

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    name: str
    address: str
    phone: str

class ProcessOrderRequest(BaseModel):
    session_id: str
    user_input: str
    username: str | None = None
    password: str | None = None