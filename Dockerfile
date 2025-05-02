# Multi-stage build for TikTok Downloader app
# Stage 1: Build frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build backend with frontend
FROM python:3.11-slim
WORKDIR /app

# Install Node.js and other dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy start script first so we can verify it exists
COPY start.sh ./
RUN chmod +x ./start.sh && ls -la ./start.sh

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build
COPY --from=frontend-build /app/.next ./frontend/.next
COPY --from=frontend-build /app/public ./frontend/public
COPY --from=frontend-build /app/package.json ./frontend/
COPY --from=frontend-build /app/node_modules ./frontend/node_modules

# Create necessary directories
RUN mkdir -p downloads logs

# Expose ports
EXPOSE 3000 8000

# Start both services
CMD ["./start.sh"] 