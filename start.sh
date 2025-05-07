#!/bin/bash

# Start Nginx
nginx

# Start the backend API on port 8001
cd /app/backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 2 &

# Start the frontend on port 3000
cd /app/frontend
NODE_ENV=production node .next/standalone/server.js &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $? 