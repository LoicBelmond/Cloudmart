from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    description: Optional[str] = None


class CartItem(BaseModel):
    id: str
    user_id: str
    product_id: str
    quantity: int


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float


class Order(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    status: str = "confirmed"
    total: float
