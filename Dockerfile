# Multi-stage build for TikTok Downloader app
# Stage 1: Build frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build backend with frontend
FROM node:18-alpine
WORKDIR /app

# Install Python and dependencies
RUN apk add --no-cache python3 py3-pip ffmpeg

# Fix for externally managed environment
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Alternatively, create and use a virtual environment
# RUN python3 -m venv /venv
# ENV PATH="/venv/bin:$PATH"
# RUN pip3 install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build
COPY --from=frontend-build /app/.next ./frontend/.next
COPY --from=frontend-build /app/public ./frontend/public
COPY --from=frontend-build /app/package.json ./frontend/
COPY --from=frontend-build /app/node_modules ./frontend/node_modules

# Create necessary directories
RUN mkdir -p downloads logs

# Copy start script
COPY start.sh .
RUN chmod +x start.sh

# Expose ports
EXPOSE 3000 8000

# Start both services
CMD ["./start.sh"] 