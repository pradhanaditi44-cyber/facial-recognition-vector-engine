FROM python:3.11-slim

# Install system dependencies required for building C extensions (like psycopg2 and face recognition tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Installed fastapi, uvicorn, pydantic, and psycopg2-binary for database communication
RUN pip install --no-cache-dir fastapi uvicorn pydantic psycopg2-binary

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]