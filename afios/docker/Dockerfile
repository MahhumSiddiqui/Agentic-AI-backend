FROM python:3.11-slim

WORKDIR /app

# Prevent Python buffering + improve pip reliability
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_DEFAULT_TIMEOUT=300

# 🔧 System dependencies (CRITICAL for ML packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install pip tooling first (better caching)
RUN pip install --upgrade pip setuptools wheel

# Copy only requirements first (for caching layer)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --retries 10 --timeout 300 -r requirements.txt

# Copy full project
COPY afios/ ./afios/

# Run API
CMD ["uvicorn", "afios.main:app", "--host", "0.0.0.0", "--port", "8000"]