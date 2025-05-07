FROM node:18-alpine as frontend

WORKDIR /app/frontend
COPY app/web/package*.json ./
RUN npm install

COPY app/web/ .
RUN npm run build

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Set up backend
WORKDIR /app/backend
COPY app/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY app/api/ .

# Create necessary directories
RUN mkdir -p downloads logs config

# Copy frontend build from previous stage
COPY --from=frontend /app/frontend/.next/standalone /app/frontend
COPY --from=frontend /app/frontend/.next/static /app/frontend/.next/static
COPY --from=frontend /app/frontend/public /app/frontend/public

# Set up Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Environment variables
ENV PORT=8000
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

# Expose port
EXPOSE 8000

# Copy startup script
COPY start.sh /app/backend/start.sh
RUN chmod +x /app/backend/start.sh

WORKDIR /app/backend
CMD ["./start.sh"] 