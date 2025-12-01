from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

# keep your existing imports:
# from .database import get_cosmos_client
# from .models import Product, ...

app = FastAPI()

# ========== Frontend paths ==========
BASE_DIR = Path(__file__).resolve().parent.parent  # /app
FRONTEND_DIR = BASE_DIR / "frontend"               # /app/frontend

# Serve static assets if you have any (CSS/JS)
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    index_file = FRONTEND_DIR / "index.html"
    # If index.html is missing, return a simple message instead of crashing
    if not index_file.exists():
        return HTMLResponse("<h1>CloudMart</h1><p>index.html not found in /frontend</p>")
    return FileResponse(index_file)


@app.get("/health")
async def health():
    return {"status": "ok", "message": "CloudMart backend is running on Azure"}
