FROM python:3.11-slim

WORKDIR /app

# 1) Copy requirements from the correct path (relative to repo root)
COPY applications/backend/requirements.txt .

# 2) Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy app code from the correct path
COPY applications/backend/app ./app

# Make sure Python can import the "app" package
ENV PYTHONPATH=/app
ENV PORT=80
EXPOSE 80

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]



