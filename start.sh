#!/bin/bash
# Start script for TikTok Downloader

# Print debugging information
echo "Starting TikTok Downloader..."
echo "Current directory: $(pwd)"
echo "Files in current directory: $(ls -la)"

# Create necessary directories if they don't exist
mkdir -p downloads logs

# Set default API URL if not provided
if [ -z "$NEXT_PUBLIC_API_URL" ]; then
  export NEXT_PUBLIC_API_URL="/api/v1"
  echo "Setting default NEXT_PUBLIC_API_URL: $NEXT_PUBLIC_API_URL"
fi

# Print environment variables for debugging (without sensitive values)
echo "Environment: $ENV"
echo "Frontend URL: $FRONTEND_URL"
echo "API key required: $REQUIRE_API_KEY"
echo "CORS settings configured"

# Start the backend service
cd /app
echo "Starting backend service..."
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Verify backend is running
sleep 5
if ! kill -0 $BACKEND_PID 2>/dev/null; then
  echo "ERROR: Backend failed to start properly"
  # Check logs
  tail -n 20 logs/*
  exit 1
fi

# Start the frontend service
cd /app/frontend
echo "Starting frontend service..."
export PORT=3000
npm start &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

# Verify frontend is running
sleep 5
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
  echo "ERROR: Frontend failed to start properly"
  # Kill backend
  kill -TERM $BACKEND_PID 2>/dev/null
  exit 1
fi

# Handle graceful shutdown
terminate() {
  echo "Received SIGTERM or SIGINT, shutting down services..."
  kill -TERM $BACKEND_PID 2>/dev/null
  kill -TERM $FRONTEND_PID 2>/dev/null
  wait $BACKEND_PID 2>/dev/null
  wait $FRONTEND_PID 2>/dev/null
  echo "All services stopped, exiting."
  exit 0
}

trap terminate SIGTERM SIGINT

# Keep script running
echo "Both services started, waiting..."
wait 