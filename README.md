# TikTok and Instagram Downloader

This project is a comprehensive solution for downloading videos from TikTok and Instagram using Python and the `yt-dlp` library. It includes both backend and frontend components to facilitate video downloading and management.

## Features

- **TikTok Video Downloading**: Download single or multiple TikTok videos, save them in high quality, and automatically name and organize files.
- **Instagram Content Downloading**: Download Instagram posts, reels, and stories, with support for carousel posts and optional authentication for private content.
- **CSV Export**: Export metadata of downloaded content to CSV files.
- **Web Interface**: A Next.js frontend for interacting with the downloader.
- **Rate Limiting**: Built-in rate limiting to prevent abuse.
- **API Documentation**: Interactive Swagger UI documentation.
- **Docker Support**: Easy deployment with Docker and Docker Compose.
- **Security Features**: API key authentication, CORS protection, and secure file handling.

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
DOWNLOAD_EXPIRY_HOURS=24
VERIFY_SSL=true

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000
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

## Security Features

- Rate limiting per IP address
- API key authentication for admin endpoints
- CORS protection
- File size limits
- Download retention policies
- SSL/TLS encryption

## File Structure

```
.
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   │   └── services/     # Business logic
│   └── Dockerfile
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
