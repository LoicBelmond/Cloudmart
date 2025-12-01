# applications/backend/Dockerfile

# 1. Base image
FROM python:3.11-slim

# 2. Workdir inside the container
WORKDIR /app

# 3. Install system deps (optional but useful for SSL, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements and install
COPY applications/backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY applications/backend/app ./app

# 6. Environment & port
ENV PORT=80
EXPOSE 80

# 7. Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
