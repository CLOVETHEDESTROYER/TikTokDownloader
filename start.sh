#!/bin/bash
# Start script for TikTok Downloader

# Print debugging information
echo "Starting TikTok Downloader..."
echo "Current directory: $(pwd)"
echo "Files in current directory: $(ls -la)"

# Start the backend service
cd /app
echo "Starting backend service..."
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Start the frontend service
cd /app/frontend
echo "Starting frontend service..."
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