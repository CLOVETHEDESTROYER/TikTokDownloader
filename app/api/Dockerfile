FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && ffmpeg -version  # Verify FFmpeg installation

# Set up backend
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY app/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY app/api/app ./app
COPY app/api/config ./config

# Create necessary directories with proper permissions
RUN mkdir -p downloads logs && \
    chmod -R 777 downloads logs

# Environment variables
ENV PORT=8001
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV ENV=development
ENV DEBUG=true
ENV DOWNLOAD_FOLDER=/app/downloads
ENV LOG_FOLDER=/app/logs

# Expose port
EXPOSE 8001

# Start the application in development mode
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"] 