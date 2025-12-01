# applications/backend/app/main.py

from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uuid

app = FastAPI(
    title="CloudMart API",
    version="1.0.0",
    description="Simplified CloudMart backend for CSP451 Milestone 3",
)

# --------------------------
# Pydantic models
# --------------------------


class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float


class CartItem(BaseModel):
    id: str
    user_id: str
    product_id: str
    quantity: int = Field(gt=0)


class Order(BaseModel):
    id: str
    user_id: str
    items: List[CartItem]
    status: str = "confirmed"


# --------------------------
# Fake in-memory “database”
# (keeps app stable even without Cosmos)
# --------------------------

PRODUCTS: List[Product] = [
    Product(id="1", name="Laptop", category="Electronics", price=999.99),
    Product(id="2", name="Headphones", category="Electronics", price=199.99),
    Product(id="3", name="Running Shoes", category="Sports", price=89.99),
    Product(id="4", name="Backpack", category="Accessories", price=49.99),
]

CART_ITEMS: List[CartItem] = []
ORDERS: List[Order] = []


# --------------------------
# Basic endpoints
# --------------------------


@app.get("/", include_in_schema=False)
async def root():
    """Simple root for browser test."""
    return {"message": "CloudMart backend is running on Azure"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


# --------------------------
# Products API
# --------------------------


@app.get("/api/v1/products", response_model=List[Product])
async def list_products(category: Optional[str] = None) -> List[Product]:
    """
    List all products (optionally filter by category).
    """
    if category:
        return [p for p in PRODUCTS if p.category.lower() == category.lower()]
    return PRODUCTS


@app.get("/api/v1/products/{product_id}", response_model=Product)
async def get_product(product_id: str) -> Product:
    """
    Get single product by id.
    """
    for p in PRODUCTS:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/api/v1/categories", response_model=List[str])
async def list_categories() -> List[str]:
    """
    List all unique categories.
    """
    return sorted({p.category for p in PRODUCTS})


# --------------------------
# Cart API
# --------------------------


@app.get("/api/v1/cart", response_model=List[CartItem])
async def get_cart(user_id: str = "demo") -> List[CartItem]:
    """
    Get all cart items for a user (default demo user).
    """
    return [item for item in CART_ITEMS if item.user_id == user_id]


@app.post("/api/v1/cart/items", response_model=CartItem, status_code=201)
async def add_cart_item(
    product_id: str,
    quantity: int = 1,
    user_id: str = "demo",
) -> CartItem:
    """
    Add an item to the cart.
    """
    # Validate product exists
    product = next((p for p in PRODUCTS if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    item = CartItem(
        id=str(uuid.uuid4()),
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
    )
    CART_ITEMS.append(item)
    return item


@app.delete("/api/v1/cart/items/{item_id}")
async def delete_cart_item(item_id: str, user_id: str = "demo"):
    """
    Remove an item from the cart.
    """
    global CART_ITEMS
    before = len(CART_ITEMS)
    CART_ITEMS = [
        item for item in CART_ITEMS if not (item.id == item_id and item.user_id == user_id)
    ]
    if len(CART_ITEMS) == before:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"status": "deleted"}


# --------------------------
# Orders API
# --------------------------


@app.post("/api/v1/orders", response_model=Order, status_code=201)
async def create_order(user_id: str = "demo") -> Order:
    """
    Create an order from the current cart.
    """
    user_cart = [item for item in CART_ITEMS if item.user_id == user_id]
    if not user_cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = Order(
        id=str(uuid.uuid4()),
        user_id=user_id,
        items=user_cart,
        status="confirmed",
    )
    ORDERS.append(order)

    # Clear the cart for that user
    global CART_ITEMS
    CART_ITEMS = [item for item in CART_ITEMS if item.user_id != user_id]

    return order


@app.get("/api/v1/orders", response_model=List[Order])
async def list_orders(user_id: str = "demo") -> List[Order]:
    """
    List all orders for a user.
    """
    return [order for order in ORDERS if order.user_id == user_id]
