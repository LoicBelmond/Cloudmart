from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from .database import init_cosmos, products_container
from .models import Product, CartItem, Order, OrderItem
from .services import products, cart, orders

app = FastAPI(title="CloudMart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_cosmos()


# ---------- FRONTEND (simple HTML) ----------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    prods = products.get_all_products()
    # Very simple HTML to meet “frontend” requirement
    html_items = "".join(
        f"<li>{p.name} - ${p.price} ({p.category})</li>" for p in prods
    )
    html = f"""
    <html>
      <head><title>CloudMart</title></head>
      <body>
        <h1>CloudMart Products</h1>
        <ul>{html_items}</ul>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


# ---------- HEALTH ----------

@app.get("/health")
async def health():
    status = {"status": "ok", "cosmos": "not_configured"}
    if products_container:
        status["cosmos"] = "connected"
    return status


# ---------- PRODUCTS API ----------

@app.get("/api/v1/products", response_model=list[Product])
async def list_products(category: str | None = None):
    return products.get_all_products(category)


@app.get("/api/v1/products/{product_id}", response_model=Product)
async def get_single_product(product_id: str):
    prod = products.get_product(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod


@app.get("/api/v1/categories")
async def list_categories():
    prods = products.get_all_products()
    cats = sorted(set(p.category for p in prods))
    return cats


# ---------- CART API (using fixed demo user 'demo') ----------

USER_ID = "demo"

@app.get("/api/v1/cart", response_model=list[CartItem])
async def get_cart_items():
    return cart.get_cart(USER_ID)


@app.post("/api/v1/cart/items", response_model=CartItem)
async def add_cart_item(item: CartItem):
    item.user_id = USER_ID
    return cart.add_to_cart(item)


@app.delete("/api/v1/cart/items/{item_id}")
async def remove_cart_item(item_id: str):
    cart.remove_from_cart(USER_ID, item_id)
    return {"status": "removed"}


# ---------- ORDERS ----------

@app.post("/api/v1/orders", response_model=Order)
async def create_order_endpoint(order: Order):
    return orders.create_order(order)


@app.get("/api/v1/orders", response_model=list[Order])
async def list_orders_endpoint():
    return orders.list_orders(USER_ID)
