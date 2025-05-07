#!/bin/bash
# Build the app
npm run build

# Set production environment variables
export NODE_ENV=production
export NEXT_PUBLIC_API_URL=/api/v1
export PORT=3000

# Start in production mode
npm start 