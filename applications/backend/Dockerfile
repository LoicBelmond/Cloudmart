# Lightweight Python image
FROM python:3.11-slim

# Work directory in the container
WORKDIR /app

# System deps (optional but helpful if you add more packages later)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Python dependencies
# -----------------------------
# Place requirements.txt in applications/backend/requirements.txt
COPY applications/backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Application code
# -----------------------------
# Backend (FastAPI) code
COPY applications/backend/app ./app

# Frontend static files (index.html lives here)
COPY applications/frontend ./frontend

# -----------------------------
# Runtime configuration
# -----------------------------
ENV PORT=80
EXPOSE 80

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
