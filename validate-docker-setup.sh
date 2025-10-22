#!/bin/bash
# Script to validate Docker setup for TikTok Downloader

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===== Validating Docker Setup for TikTok Downloader =====${NC}"
echo ""

# Check for required files
echo -e "${BLUE}Checking for required files...${NC}"
REQUIRED_FILES=(
  "docker-compose.yml"
  "app/api/Dockerfile"
  "app/api/requirements.txt"
  "app/api/app/services/tiktok.py"
)

ALL_FILES_FOUND=true
for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo -e "${GREEN}✅ Found: $file${NC}"
  else
    echo -e "${RED}❌ Missing: $file${NC}"
    ALL_FILES_FOUND=false
  fi
done

if [ "$ALL_FILES_FOUND" = false ]; then
  echo -e "${RED}Some required files are missing. Please ensure your repository structure matches the expected layout.${NC}"
  exit 1
fi

echo ""
echo -e "${BLUE}Checking Docker installation...${NC}"
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
  echo -e "${GREEN}✅ Docker and docker-compose are installed${NC}"
else
  echo -e "${RED}❌ Docker and/or docker-compose are not installed${NC}"
  echo -e "${YELLOW}Please install Docker and docker-compose before continuing.${NC}"
  exit 1
fi

echo ""
echo -e "${BLUE}Checking yt-dlp version in requirements.txt...${NC}"
YT_DLP_VERSION=$(grep "yt-dlp==" app/api/requirements.txt | cut -d "=" -f 3)
if [ -z "$YT_DLP_VERSION" ]; then
  echo -e "${YELLOW}⚠️ yt-dlp not found in requirements.txt or version format is unexpected${NC}"
  echo -e "${YELLOW}Please ensure yt-dlp is included with version 2024.3.10 or newer${NC}"
else
  echo -e "${GREEN}✅ Found yt-dlp version $YT_DLP_VERSION${NC}"
  if [[ "$YT_DLP_VERSION" < "2024.3.10" ]]; then
    echo -e "${YELLOW}⚠️ yt-dlp version is outdated. Version 2024.3.10 or newer is recommended.${NC}"
  fi
fi

echo ""
echo -e "${BLUE}Checking for FFmpeg in Dockerfile...${NC}"
if grep -q "ffmpeg" app/api/Dockerfile; then
  echo -e "${GREEN}✅ FFmpeg is included in Dockerfile${NC}"
else
  echo -e "${YELLOW}⚠️ FFmpeg not found in Dockerfile${NC}"
  echo -e "${YELLOW}Please add ffmpeg to apt-get install list in app/api/Dockerfile${NC}"
fi

echo ""
echo -e "${BLUE}Checking docker-compose.yml configuration...${NC}"
# Check for DOWNLOAD_NO_WATERMARK environment variable
if grep -q "DOWNLOAD_NO_WATERMARK=true" docker-compose.yml; then
  echo -e "${GREEN}✅ DOWNLOAD_NO_WATERMARK environment variable is configured${NC}"
else
  echo -e "${YELLOW}⚠️ DOWNLOAD_NO_WATERMARK environment variable not found in docker-compose.yml${NC}"
  echo -e "${YELLOW}Please add '- DOWNLOAD_NO_WATERMARK=true' to backend environment variables${NC}"
fi

# Check for volume configuration
if grep -q "downloads:/app/downloads" docker-compose.yml; then
  echo -e "${GREEN}✅ Volumes configuration looks good${NC}"
else
  echo -e "${YELLOW}⚠️ Downloads volume configuration not found${NC}"
  echo -e "${YELLOW}Please add appropriate volume mapping for downloads folder${NC}"
fi

echo ""
echo -e "${BLUE}Checking TikTok download implementation...${NC}"
if grep -q "download_without_watermark" app/api/app/services/tiktok.py; then
  echo -e "${GREEN}✅ TikTok watermark removal is implemented${NC}"
else
  echo -e "${YELLOW}⚠️ TikTok watermark removal may not be properly implemented${NC}"
  echo -e "${YELLOW}Please ensure download_without_watermark option is used in tiktok.py${NC}"
fi

echo ""
if [ "$ALL_FILES_FOUND" = true ]; then
  echo -e "${GREEN}===== Validation Complete =====${NC}"
  echo -e "${GREEN}Your Docker setup for TikTok downloader appears to be valid.${NC}"
  echo -e "${GREEN}To apply the configuration, run:${NC}"
  echo -e "  ./update-docker.sh"
  echo -e "${GREEN}To test after updating, run:${NC}"
  echo -e "  ./test-docker-tiktok.sh"
else
  echo -e "${RED}===== Validation Failed =====${NC}"
  echo -e "${RED}Please fix the issues mentioned above before continuing.${NC}"
  exit 1
fi

echo "" 