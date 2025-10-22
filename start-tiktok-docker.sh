#!/bin/bash
# Script to start the TikTok Docker container and test its functionality

echo "===== Starting TikTok Downloader in Docker ====="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker and try again."
  exit 1
fi

# Stop any existing containers
echo "Stopping any existing containers..."
docker-compose -f docker-compose.tiktok.yml down

# Create the downloads directory if it doesn't exist
mkdir -p downloads

# Start the container
echo "Starting TikTok Downloader container..."
docker-compose -f docker-compose.tiktok.yml up -d

# Wait for the container to start
echo "Waiting for container to start..."
sleep 10

# Check if the container is running
CONTAINER_ID=$(docker-compose -f docker-compose.tiktok.yml ps -q tiktok-backend)
if [ -z "$CONTAINER_ID" ]; then
  echo "Error: Failed to start TikTok Downloader container."
  exit 1
fi

echo "Container started with ID: $CONTAINER_ID"

# Check if the API is responding
echo "Checking API health..."
HEALTH_CHECK=$(curl -s http://localhost:8001/health)
if [[ $HEALTH_CHECK == *"ok"* ]]; then
  echo "✅ API is healthy!"
else
  echo "⚠️ API health check failed. Container might still be starting up."
  echo "Check logs with: docker-compose -f docker-compose.tiktok.yml logs"
fi

# Check for required components
echo "Checking for FFmpeg..."
docker exec $CONTAINER_ID ffmpeg -version | head -n 1
if [ $? -ne 0 ]; then
  echo "❌ FFmpeg is not properly installed"
else
  echo "✅ FFmpeg is properly installed"
fi

echo "Checking for yt-dlp..."
docker exec $CONTAINER_ID pip show yt-dlp | grep Version
if [ $? -ne 0 ]; then
  echo "❌ yt-dlp is not properly installed"
else
  echo "✅ yt-dlp is properly installed"
fi

echo "Checking for DOWNLOAD_NO_WATERMARK environment variable..."
docker exec $CONTAINER_ID env | grep DOWNLOAD_NO_WATERMARK
if [ $? -ne 0 ]; then
  echo "❌ DOWNLOAD_NO_WATERMARK environment variable is not set"
else
  echo "✅ DOWNLOAD_NO_WATERMARK environment variable is set"
fi

echo "===== TikTok Downloader Setup Complete ====="
echo ""
echo "Your TikTok Downloader is now running in Docker."
echo "Access the API at: http://localhost:8001"
echo ""
echo "To use the TikTok downloader API, send a POST request to:"
echo "  http://localhost:8001/api/v1/download"
echo "With the body:"
echo '  {"url": "https://www.tiktok.com/your-video-url", "platform": "tiktok", "quality": "high"}'
echo ""
echo "To view logs, run:"
echo "  docker-compose -f docker-compose.tiktok.yml logs -f"
echo ""
echo "To stop the container, run:"
echo "  docker-compose -f docker-compose.tiktok.yml down" 