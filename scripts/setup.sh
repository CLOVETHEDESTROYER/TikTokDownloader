#!/bin/bash

# Create necessary directories
mkdir -p app/api/downloads app/api/logs

# Set up Python virtual environment
cd app/api
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create example .env file if it doesn't exist
if [ ! -f .env ]; then
    cat > .env << EOL
API_SECRET_KEY=development-secret-key
WEBSITE_API_KEY=development-api-key
DOWNLOAD_FOLDER=downloads
FRONTEND_URL=http://localhost:3000
EOL
    echo "Created example .env file"
fi

# Set up frontend (if it exists)
cd ../web
if [ -f package.json ]; then
    npm install
    
    # Create example .env.local file if it doesn't exist
    if [ ! -f .env.local ]; then
        cat > .env.local << EOL
NEXT_PUBLIC_API_URL=/api/v1
NEXT_PUBLIC_WEBSITE_API_KEY=development-api-key
EOL
        echo "Created example .env.local file"
    fi
fi

echo "Setup complete! You can now start the development servers:"
echo "1. Backend: cd app/api && uvicorn app.main:app --reload"
echo "2. Frontend: cd app/web && npm run dev" 