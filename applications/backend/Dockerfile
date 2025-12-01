FROM python:3.11-slim

# 1) Work dir inside container
WORKDIR /app

# 2) Install Python deps
COPY applications/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy backend code
COPY applications/backend/app ./app

# 4) Copy frontend code
COPY applications/frontend ./frontend

# 5) Expose HTTP port
ENV PORT=80
EXPOSE 80

# 6) Start FastAPI with Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
