FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY applications/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY applications/backend/app ./app

ENV PORT=80
EXPOSE 80

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
