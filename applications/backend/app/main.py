from typing import List
from pydantic import BaseModel

# ---------- Product model & in-memory data ----------

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    description: str | None = None
    image_url: str | None = None


# Temporary in-memory products (so the frontend always works)
FAKE_PRODUCTS: List[Product] = [
    Product(
        id="1",
        name="Wireless Headphones",
        category="Electronics",
        price=79.99,
        description="Bluetooth over-ear headphones with noise isolation.",
        image_url="https://via.placeholder.com/200x200?text=Headphones",
    ),
    Product(
        id="2",
        name="Gaming Mouse",
        category="Electronics",
        price=49.99,
        description="RGB gaming mouse with 6 programmable buttons.",
        image_url="https://via.placeholder.com/200x200?text=Mouse",
    ),
    Product(
        id="3",
        name="Water Bottle",
        category="Home",
        price=19.99,
        description="Insulated stainless-steel bottle, 750 ml.",
        image_url="https://via.placeholder.com/200x200?text=Bottle",
    ),
]


@app.get("/api/v1/products", response_model=List[Product])
async def list_products():
    """
    Return a list of products.

    NOTE: right now this uses in-memory data (FAKE_PRODUCTS)
    so the UI works even if Cosmos DB is empty or misconfigured.
    Later you can replace this with a Cosmos DB query.
    """
    return FAKE_PRODUCTS
