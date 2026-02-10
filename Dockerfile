# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy entire project
COPY . .

# Create data directory
RUN mkdir -p data articles

# Set Flask app and environment for web server
ENV FLASK_APP=tech_crawler/web/app.py

# Expose port for web server
EXPOSE 5000

# Default command: run the crawler
CMD ["python", "main.py"]
