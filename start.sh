#!/bin/bash

# Create necessary directories
mkdir -p /app/backend/downloads
mkdir -p /app/backend/logs
mkdir -p /var/log/nginx

# Start Nginx
nginx

# Start the backend API on port 8001
cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 2 &

# Wait for backend to be ready
while ! curl -s http://localhost:8001/health > /dev/null; do
    echo "Waiting for backend to be ready..."
    sleep 1
done

# Start the frontend on port 3000
cd /app/frontend
PORT=3000 node server.js &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $? 