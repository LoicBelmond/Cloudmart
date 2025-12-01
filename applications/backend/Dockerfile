# applications/backend/Dockerfile
# Build context is the repository root.
# Example local build:
#   docker build -t cloudmart-api-local -f applications/backend/Dockerfile .

FROM python:3.11-slim

# Avoid interactive prompts & keep image small
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# -------------------------------------------------------
# Install Python dependencies
# -------------------------------------------------------

# Copy only requirements first so Docker can cache this layer
COPY applications/backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------------
# Copy application code
# -------------------------------------------------------

COPY applications/backend/app ./app

# -------------------------------------------------------
# Runtime configuration
# -------------------------------------------------------

ENV PORT=80
EXPOSE 80

# Use uvicorn to run the FastAPI app
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
