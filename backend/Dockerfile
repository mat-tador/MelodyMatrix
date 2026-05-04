# FastAPI chatbot backend
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose API port
EXPOSE 5001

# Health check (must match your FastAPI route)
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5001/api/health', timeout=4)"

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]