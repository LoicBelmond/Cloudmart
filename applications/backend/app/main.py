from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .database import get_cosmos_client  # keep your existing imports
from .models import Product            # and any others you had

app = FastAPI()

# =========================
# Frontend paths + static
# =========================
# current file: /app/app/main.py
# app root:      /app
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Serve static files (CSS, JS, etc.) from /static
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    """
    Return the frontend HTML page instead of JSON.
    """
    index_file = FRONTEND_DIR / "index.html"
    return FileResponse(index_file)


# =========================
# Health check
# =========================
@app.get("/health")
async def health():
    return {"status": "ok", "message": "CloudMart backend is running on Azure"}


# =========================
# Example API endpoints
# (keep your existing ones, or use these)
# =========================
@app.get("/api/v1/products")
async def list_products():
    client = get_cosmos_client()
    database = client.get_database_client("cloudmart")
    container = database.get_container_client("products")

    items = list(container.read_all_items())
    return items
