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
  exit 1
fi

# Verify the backend is responding to health checks
echo "Testing backend health check..."
HEALTH_CHECK=$(curl -s http://localhost:8000/health)
echo "Health check response: $HEALTH_CHECK"

# Start the frontend service
cd /app/frontend
echo "Starting frontend service..."
export PORT=3000
npm start &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

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