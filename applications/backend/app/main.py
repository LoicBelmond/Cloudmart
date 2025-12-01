from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Paths for frontend
# -----------------------------------------------------------------------------
# /app/app/main.py  -> parent().parent() = /app
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# -----------------------------------------------------------------------------
# FastAPI app
# -----------------------------------------------------------------------------
app = FastAPI(
    title="CloudMart API",
    version="1.0.0",
    description="Simple CloudMart backend + static frontend for CSP451 lab.",
)

# Serve static frontend files (CSS/JS if you add them later)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    """
    Return the CloudMart frontend page.
    This serves applications/frontend/index.html inside the Docker image.
    """
    index_file = FRONTEND_DIR / "index.html"
    if not index_file.exists():
        # Fallback so container still responds even if file is missing
        return {"message": "CloudMart backend is running on Azure (frontend file not found)."}
    return FileResponse(index_file)


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------
class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str


class CartItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)
    price_each: float


class Order(BaseModel):
    id: str
    items: List[OrderItem]
    total: float
    status: str = "created"


class OrderCreate(BaseModel):
    items: List[CartItem]


# -----------------------------------------------------------------------------
# In-memory "database" (good enough for the lab demo)
# -----------------------------------------------------------------------------
PRODUCTS: List[Product] = [
    Product(
        id="p1",
        name="Azure Notebook",
        description="Cloud-blue notebook with the Azure logo.",
        price=9.99,
        category="Stationery",
    ),
    Product(
        id="p2",
        name="Cloud Hoodie",
        description="Warm hoodie for late-night coding.",
        price=39.50,
        category="Apparel",
    ),
    Product(
        id="p3",
        name="Dev Mug",
        description="Big mug for big debugging sessions.",
        price=14.25,
        category="Accessories",
    ),
]

ORDERS: List[Order] = []


# -----------------------------------------------------------------------------
# Health check
# -----------------------------------------------------------------------------
@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "message": "CloudMart backend is running on Azure"}


# -----------------------------------------------------------------------------
# Products endpoints
# -----------------------------------------------------------------------------
@app.get("/api/v1/products", response_model=List[Product])
async def list_products() -> List[Product]:
    """
    Return all products.
    The frontend calls this to render the product grid.
    """
    return PRODUCTS


@app.get("/api/v1/products/{product_id}", response_model=Product)
async def get_product(product_id: str) -> Product:
    for p in PRODUCTS:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")


# -----------------------------------------------------------------------------
# Cart + Order endpoints (simple demo)
# -----------------------------------------------------------------------------
@app.post("/api/v1/orders", response_model=Order, status_code=201)
async def create_order(payload: OrderCreate) -> Order:
    """
    Create an order from cart items.
    For the lab we keep it in memory only.
    """
    order_items: List[OrderItem] = []

    for item in payload.items:
        # Find product and calculate line price
        product = next((p for p in PRODUCTS if p.id == item.product_id), None)
        if product is None:
            raise HTTPException(status_code=400, detail=f"Unknown product_id: {item.product_id}")
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price_each=product.price,
            )
        )

    total = sum(i.quantity * i.price_each for i in order_items)
    order = Order(id=str(uuid4()), items=order_items, total=total, status="created")
    ORDERS.append(order)
    return order


@app.get("/api/v1/orders", response_model=List[Order])
async def list_orders() -> List[Order]:
    # Only from memory – enough to prove endpoint works
    return ORDERS
