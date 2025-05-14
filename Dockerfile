FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p downloads logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DOWNLOAD_FOLDER=/app/downloads
ENV LOG_FOLDER=/app/logs

# Expose port for the Flask web interface
EXPOSE 5000

# Set the entrypoint
CMD ["python", "flask_web_ui.py"] 