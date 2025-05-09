#!/bin/bash

# Create required directories
mkdir -p downloads
mkdir -p logs
mkdir -p config

# Copy placeholder .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating placeholder .env file..."
    cat > .env << EOL
# API configuration
API_SECRET_KEY=development_secret_key
WEBSITE_API_KEY=test_api_key_123
ADMIN_API_KEY=admin_test_key_456
ENV=development
REQUIRE_API_KEY=true
DEBUG=true

# Server settings
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Downloads
DOWNLOAD_FOLDER=downloads
DOWNLOAD_EXPIRY_MINUTES=60

# CORS settings
FRONTEND_URL=http://localhost:3000
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,OPTIONS
CORS_ALLOW_HEADERS=Content-Type,Authorization,X-Request-ID,X-API-Key,Accept,Origin,Cache-Control
CORS_EXPOSE_HEADERS=X-Request-ID

# Instagram settings
INSTAGRAM_COOKIES_FILE=config/instagram_cookies.txt
INSTAGRAM_MAX_RETRIES=3
INSTAGRAM_TIMEOUT=30

# Rate limiting
RATE_LIMIT_PER_MINUTE=60

# Monitoring
ENABLE_METRICS=false
EOL
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
echo "Starting API server..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Note: Press CTRL+C to stop the server 