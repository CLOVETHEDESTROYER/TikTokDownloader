FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && ffmpeg -version  # Verify FFmpeg installation

# Set up backend working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY app/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the latest yt-dlp version for TikTok watermark removal
RUN pip install --no-cache-dir yt-dlp>=2025.4.30

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
ENV ENV=production
ENV DEBUG=false
ENV DOWNLOAD_NO_WATERMARK=true
ENV DOWNLOAD_FOLDER=/app/downloads
ENV LOG_FOLDER=/app/logs

# Expose port
EXPOSE 8001

# Start the application in production mode (no reload, multiple workers)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"] 