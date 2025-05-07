#!/bin/bash
# Start script for TikTok Downloader

# Print debugging information
echo "Starting TikTok Downloader..."
echo "Current directory: $(pwd)"
echo "Files in current directory: $(ls -la)"

# Create necessary directories
mkdir -p downloads logs

# Make sure environment variables are set
if [ -z "$PORT" ]; then
  export PORT=8000
  echo "Setting default PORT: $PORT"
fi

# Start backend service
echo "Starting backend service..."
cd api
python -m uvicorn app.main:app --host 0.0.0.0 --port $API_PORT &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Wait for backend to be ready
sleep 3

# Test backend health
echo "Testing backend health check..."
HEALTH_RESPONSE=$(curl -s http://localhost:$API_PORT/health)
echo "Health check response: $HEALTH_RESPONSE"

# Start frontend service
echo "Starting frontend service..."
cd ../web
npm start &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

echo "Both services started, waiting..."

# Wait for either process to exit
wait -n $BACKEND_PID $FRONTEND_PID

# If we get here, one of the processes exited
echo "One of the services exited. Shutting down..."
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null 