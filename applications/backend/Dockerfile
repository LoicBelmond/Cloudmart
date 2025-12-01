FROM python:3.11-slim

WORKDIR /app

# Install backend deps
COPY applications/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY applications/backend/app ./app

# Copy frontend files
COPY applications/frontend ./frontend

ENV PYTHONPATH=/app
ENV PORT=80
EXPOSE 80

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

