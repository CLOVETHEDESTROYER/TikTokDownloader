#!/bin/bash
# Test script for TikTok watermark removal in Docker

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker and try again."
  exit 1
fi

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
  echo "Error: Docker containers are not running. Start them with: docker-compose up -d"
  exit 1
fi

# Get the backend container ID
BACKEND_CONTAINER=$(docker-compose ps -q backend)
if [ -z "$BACKEND_CONTAINER" ]; then
  echo "Error: Backend container not found."
  exit 1
fi

echo "====== Testing TikTok Watermark Removal in Docker ======"
echo ""
echo "1. Testing FFmpeg installation in container..."
docker exec $BACKEND_CONTAINER ffmpeg -version | head -n 1
if [ $? -ne 0 ]; then
  echo "  ❌ FFmpeg is not properly installed in the container"
  exit 1
else
  echo "  ✅ FFmpeg is properly installed"
fi

echo ""
echo "2. Testing yt-dlp installation in container..."
YT_DLP_VERSION=$(docker exec $BACKEND_CONTAINER pip show yt-dlp | grep Version | awk '{print $2}')
if [ -z "$YT_DLP_VERSION" ]; then
  echo "  ❌ yt-dlp is not properly installed in the container"
  exit 1
else
  echo "  ✅ yt-dlp is properly installed (Version: $YT_DLP_VERSION)"
  
  # Check if version is recent enough (2024.3.10 or higher)
  if [[ "$YT_DLP_VERSION" < "2024.3.10" ]]; then
    echo "  ⚠️ yt-dlp version is outdated. Version 2024.3.10 or newer is recommended."
  fi
fi

echo ""
echo "3. Testing environment variables..."
WATERMARK_ENV=$(docker exec $BACKEND_CONTAINER env | grep DOWNLOAD_NO_WATERMARK)
if [ -z "$WATERMARK_ENV" ]; then
  echo "  ⚠️ DOWNLOAD_NO_WATERMARK environment variable not found. This may affect watermark removal."
else
  echo "  ✅ DOWNLOAD_NO_WATERMARK environment variable is set: $WATERMARK_ENV"
fi

echo ""
echo "4. Testing API endpoints..."
# Get API health status
HEALTH_STATUS=$(curl -s http://localhost:8001/health | grep -o '"status":"ok"')
if [ -z "$HEALTH_STATUS" ]; then
  echo "  ❌ API health check failed. Backend may not be running correctly."
else
  echo "  ✅ API health check passed"
  
  # Test API version endpoint
  API_VERSION=$(curl -s http://localhost:8001/api/v1/version 2>/dev/null)
  if [ $? -eq 0 ] && [ ! -z "$API_VERSION" ]; then
    echo "  ✅ API version endpoint is working: $API_VERSION"
  else
    echo "  ⚠️ API version endpoint check failed (this is not critical)"
  fi
fi

echo ""
echo "5. Testing TikTok download module..."
# Check if the TikTok service module exists
SERVICE_CHECK=$(docker exec $BACKEND_CONTAINER ls -la /app/app/services/tiktok.py 2>/dev/null)
if [ $? -ne 0 ]; then
  echo "  ⚠️ TikTok service module not found at expected path. Service may be located elsewhere."
else
  echo "  ✅ TikTok service module exists"
  
  # Test if watermark removal logic is present
  WATERMARK_LOGIC=$(docker exec $BACKEND_CONTAINER grep -c "download_without_watermark" /app/app/services/tiktok.py)
  if [ "$WATERMARK_LOGIC" -gt 0 ]; then
    echo "  ✅ Watermark removal logic is implemented"
  else
    echo "  ⚠️ Watermark removal logic may be missing"
  fi
fi

echo ""
echo "6. Testing TikTok download endpoint (simulation only)..."
echo "  ℹ️ Not performing actual download test (would require a valid TikTok URL)"
echo "  ℹ️ To test manually, use the web interface at http://localhost:3000"
echo "  ℹ️ or test the API directly with:"
echo "  curl -X POST http://localhost:8001/api/v1/download \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -H 'X-API-Key: your_api_key' \\"
echo "    -d '{\"url\": \"https://www.tiktok.com/video-url\", \"platform\": \"tiktok\", \"quality\": \"high\"}'"

echo ""
echo "7. Volume and file permission check..."
DOWNLOADS_DIR=$(docker exec $BACKEND_CONTAINER ls -la /app/downloads)
if [ $? -ne 0 ]; then
  echo "  ⚠️ Downloads directory not found or not accessible"
else
  echo "  ✅ Downloads directory is properly configured"
  
  # Check write permissions
  docker exec $BACKEND_CONTAINER touch /app/downloads/test_file 2>/dev/null
  if [ $? -eq 0 ]; then
    echo "  ✅ Write permissions to downloads directory are correct"
    docker exec $BACKEND_CONTAINER rm /app/downloads/test_file
  else
    echo "  ❌ Write permissions to downloads directory are missing"
  fi
fi

echo ""
echo "====== Test Complete ======"
echo ""
echo "If all checks passed, your Docker setup is properly configured for TikTok watermark removal."
echo "For any warnings or errors, check the documentation in README.md" 