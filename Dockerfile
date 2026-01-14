# TikTok/Facebook Video Downloader API
# Single Dockerfile for DigitalOcean App Platform

FROM python:3.11-slim

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && ffmpeg -version

# Set up working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY app/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure latest yt-dlp for watermark removal support
RUN pip install --no-cache-dir --upgrade yt-dlp

# Copy backend application code
COPY app/api/app ./app
COPY app/api/config ./config

# Create necessary directories
RUN mkdir -p downloads logs && \
    chmod -R 777 downloads logs

# Environment variables
ENV PORT=8001
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"
ENV ENV=production
ENV DEBUG=false
ENV DOWNLOAD_NO_WATERMARK=true
ENV DOWNLOAD_FOLDER=/app/downloads
ENV LOG_FOLDER=/app/logs
ENV REQUIRE_API_KEY=false

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]
