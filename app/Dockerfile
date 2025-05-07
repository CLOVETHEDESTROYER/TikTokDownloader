# Use Node.js as base image
FROM node:18-alpine as frontend

# Set working directory
WORKDIR /app/web

# Copy frontend files
COPY web/package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY web/ .

# Build frontend
RUN npm run build

# Use Python for backend
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements and install dependencies
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY api/ api/

# Copy built frontend from previous stage
COPY --from=frontend /app/web/.next web/.next
COPY --from=frontend /app/web/public web/public
COPY --from=frontend /app/web/package.json web/

# Copy start script
COPY ../scripts/start.sh .
RUN chmod +x start.sh

# Create necessary directories
RUN mkdir -p downloads logs config

# Set environment variables
ENV PORT=3000
ENV API_PORT=8000
ENV NODE_ENV=production

# Expose ports
EXPOSE $PORT $API_PORT

# Start both services
CMD ["./start.sh"] 