# TikTok and Instagram Downloader

This project is a comprehensive solution for downloading videos from TikTok and Instagram using Python and the `yt-dlp` library. It includes both backend and frontend components to facilitate video downloading and management.

## Features

- **TikTok Video Downloading**: Download single or multiple TikTok videos, save them in high quality, and automatically name and organize files.
- **Instagram Content Downloading**: Download Instagram posts, reels, and stories, with support for carousel posts and optional authentication for private content.
- **CSV Export**: Export metadata of downloaded content to CSV files.
- **Web Interface**: A modern Next.js frontend with TypeScript and Tailwind CSS for a beautiful user experience.
- **Video Preview**: Preview videos before downloading with thumbnail and metadata display.
- **Real-time Progress**: WebSocket integration for real-time download progress updates.
- **Automatic Cleanup**: Downloaded files are automatically removed after 5 minutes to maintain server efficiency.
- **Rate Limiting Tiers**:
  - Free Tier: 50 requests, 5 downloads, 5 bulk downloads per 30 minutes
  - Premium Tier: 250 requests, 50 downloads, 10 bulk downloads per 30 minutes
  - Enterprise Tier: 1000 requests, 250 downloads, 50 bulk downloads per 30 minutes
- **Monitoring**: Prometheus metrics integration for tracking downloads, rate limits, and system performance.
- **API Documentation**: Interactive Swagger UI documentation.
- **Docker Support**: Easy deployment with Docker and Docker Compose.
- **Security Features**: API key authentication, CORS protection, secure file handling, and robust IP detection.

## Requirements

- Python 3.11+
- Node.js 18+
- `yt-dlp` library
- Docker and Docker Compose (for containerized deployment)
- FFmpeg (for video processing)
- Optional: Authentication cookies for Instagram private content

## Installation

### Local Development

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/TikTokDownloader.git
   cd TikTokDownloader
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   ```

### Docker Deployment

1. **Set up environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker compose up -d --build
   ```

## Environment Variables

### Backend (.env)

```
# API Configuration
API_SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
ADMIN_API_KEY=your-admin-key

# Server Settings
PORT=8000
WORKERS=4
ENV=production

# Download Settings
MAX_DOWNLOADS=50
MAX_CONCURRENT_DOWNLOADS=10
DOWNLOAD_EXPIRY_MINUTES=5
VERIFY_SSL=true

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
TRUSTED_PROXIES=127.0.0.1,10.0.0.0/8
RATE_LIMIT_HEADERS=X-Real-IP,X-Forwarded-For

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

## Usage

### Local Development

1. **Run the FastAPI server**:

   ```bash
   uvicorn backend.app.main:app --reload
   ```

2. **Run the Next.js frontend**:

   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the application**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
   - OpenAPI Spec: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

### Production Deployment

1. **Using Docker (Recommended)**:

   ```bash
   docker compose up -d
   ```

   This will start:

   - Frontend on port 3000
   - Backend on port 8000
   - Nginx reverse proxy on ports 80/443

2. **Manual Deployment**:
   - Set up Nginx as reverse proxy
   - Configure SSL certificates
   - Set up environment variables
   - Run the services using PM2 or similar process manager

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /api/v1/download`: Download single video
- `POST /api/v1/batch-download`: Download multiple videos
- `GET /api/v1/status/{session_id}`: Check download status
- `GET /api/v1/file/{session_id}`: Download completed file
- `GET /api/v1/quota`: Check rate limit quota
- `GET /metrics`: Prometheus metrics endpoint (protected)
- `WS /api/v1/ws/{session_id}`: WebSocket endpoint for real-time updates

## Monitoring and Metrics

The application includes Prometheus metrics for monitoring:

- Download durations and success rates
- Rate limit violations and quota usage
- Request counts by endpoint and status
- System resource utilization
- WebSocket connection statistics

Access metrics at `/metrics` endpoint (requires authentication).

## Security Features

- Tiered rate limiting with IP-based tracking
- Robust IP detection through multiple headers
- API key authentication for admin endpoints
- CORS protection
- File size limits
- Download retention policies
- SSL/TLS encryption
- Trusted proxy configuration

## File Structure

```
.
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   │   └── services/     # Business logic
│   │   └── Dockerfile
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Next.js pages
│   │   └── utils/        # Utility functions
│   └── Dockerfile
├── downloads/            # Downloaded videos
├── docker-compose.yml    # Docker Compose config
└── README.md
```

## Future Enhancements

- Watermark detection and removal
- Cloud sync options
- GUI with Tkinter
- Telegram bot integration
- Enhanced analytics dashboard
- User authentication and profiles
- Custom download quality selection
- Batch processing improvements

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## Contact

For any questions or support, please contact [your email].

---
