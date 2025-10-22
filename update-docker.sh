#!/bin/bash
# Script to update Docker implementation with TikTok download changes

# Ensure script is running from project root
if [ ! -f "docker-compose.yml" ]; then
  echo "Please run this script from the project root directory"
  exit 1
fi

echo "===== Updating Docker Implementation with TikTok Download Changes ====="

# Step 1: Verify FFmpeg is included in Dockerfile
echo "Checking FFmpeg in Dockerfile..."
if grep -q "ffmpeg" app/api/Dockerfile; then
  echo "✅ FFmpeg is already included in Dockerfile"
else
  echo "⚠️ FFmpeg not found in Dockerfile, adding it now..."
  # Add FFmpeg to the Dockerfile system dependencies
  sed -i.bak '/apt-get install/s/\(.*\)python3-dev \\/\1python3-dev \\\n    ffmpeg \\/' app/api/Dockerfile
  rm -f app/api/Dockerfile.bak
  echo "✅ FFmpeg added to Dockerfile"
fi

# Step 2: Ensure latest yt-dlp version is used
echo "Updating yt-dlp version in requirements.txt..."
YT_DLP_VERSION="2024.3.10"
if grep -q "yt-dlp==" app/api/requirements.txt; then
  sed -i.bak "s/yt-dlp==.*/yt-dlp==$YT_DLP_VERSION/" app/api/requirements.txt
  rm -f app/api/requirements.txt.bak
  echo "✅ yt-dlp updated to version $YT_DLP_VERSION"
else
  echo "⚠️ yt-dlp not found in requirements.txt, adding it now..."
  echo "yt-dlp==$YT_DLP_VERSION" >> app/api/requirements.txt
  echo "✅ yt-dlp added to requirements.txt"
fi

# Step 3: Set environment variables
echo "Configuring Docker environment variables..."
if grep -q "DOWNLOAD_NO_WATERMARK=true" docker-compose.yml; then
  echo "✅ DOWNLOAD_NO_WATERMARK environment variable already configured"
else
  # Add new environment variable for TikTok download settings
  sed -i.bak '/WEBSITE_API_KEY/a\      - DOWNLOAD_NO_WATERMARK=true' docker-compose.yml
  rm -f docker-compose.yml.bak
  echo "✅ DOWNLOAD_NO_WATERMARK environment variable added to docker-compose.yml"
fi

# Step 4: Update Docker volume configuration if needed
echo "Checking Docker volume configuration..."
if grep -q "downloads:/app/downloads" docker-compose.yml; then
  echo "✅ Volume configuration looks good"
else
  echo "⚠️ Volumes configuration not found, please add the following to your docker-compose.yml:"
  echo "  volumes:"
  echo "    - downloads:/app/downloads"
  echo ""
  echo "  And at the bottom of the file:"
  echo "  volumes:"
  echo "    downloads:"
fi

# Step 5: Ensure TikTok download service has watermark removal logic
echo "Ensuring TikTok service has watermark removal logic..."
if [ -f "app/api/app/services/tiktok.py" ]; then
  if grep -q "download_without_watermark" app/api/app/services/tiktok.py; then
    echo "✅ Watermark removal logic is already implemented"
  else
    echo "⚠️ Watermark removal logic may be missing in TikTok service"
    echo "  Please check app/api/app/services/tiktok.py and ensure it has 'download_without_watermark' option"
  fi
else
  echo "⚠️ TikTok service file not found at expected location"
  echo "  Please ensure your backend code includes proper TikTok download service"
fi

# Step 6: Update README with Docker TikTok watermark removal documentation
echo "Updating README.md with Docker TikTok watermark information..."
if grep -q "DOWNLOAD_NO_WATERMARK" README.md; then
  echo "✅ README already includes TikTok watermark removal documentation"
else
  echo "⚠️ Adding TikTok watermark removal documentation to README.md"
  # This is a simplistic approach - in a real scenario, you might want to be more careful about where this gets inserted
  README_ADD="## 🛠️ TikTok Watermark Removal in Docker\n\nThis project supports automatic TikTok watermark removal when running in Docker. The following features are enabled:\n\n- FFmpeg installed in container for video processing\n- Latest yt-dlp version ($YT_DLP_VERSION) for TikTok download support\n- DOWNLOAD_NO_WATERMARK environment variable for enhanced watermark removal\n\nTo test the TikTok watermark removal functionality, run:\n\n\`\`\`bash\n./test-docker-tiktok.sh\n\`\`\`"
  
  # Find a good place to insert this - after the TikTok Downloader Implementation section
  if grep -q "TikTok Downloader Implementation" README.md; then
    sed -i.bak "/TikTok Downloader Implementation/,/^$/!b;/^$/a\\$README_ADD\\n" README.md
  else
    # Otherwise add it before the Contributing section
    sed -i.bak "/Contributing/i\\$README_ADD\\n" README.md
  fi
  
  rm -f README.md.bak
  echo "✅ TikTok watermark removal documentation added to README.md"
fi

# Step 7: Rebuild Docker images?
echo ""
echo "Would you like to rebuild Docker images now? (y/n)"
read -r rebuild
if [[ $rebuild == "y" ]]; then
  echo "Rebuilding Docker images..."
  docker-compose down
  docker-compose build --no-cache
  docker-compose up -d
  echo "✅ Docker rebuild complete!"
  echo ""
  echo "Running test script to verify configuration..."
  ./test-docker-tiktok.sh
else
  echo "Skipping Docker rebuild. To rebuild later, run:"
  echo "  docker-compose build --no-cache"
  echo "  docker-compose up -d"
fi

echo ""
echo "===== TikTok Download Implementation Update Complete ====="
echo "Your Docker implementation has been updated to support TikTok watermark removal."
echo "To test your configuration, run: ./test-docker-tiktok.sh"
echo "" 