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
- **Enhanced Progress Tracking**:
  - Real-time download progress with multiple stages (analyzing, downloading, processing)
  - Visual progress indicators with status icons for downloading, completion, and errors
  - Dark mode compatible progress UI
  - WebSocket integration for real-time progress updates
  - Automatic cleanup tracking with expiration countdown

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
WEBSITE_API_KEY=your-website-key
API_KEY_HEADER_NAME=X-API-Key
REQUIRE_API_KEY=true

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

# CORS Settings
FRONTEND_URL=https://your-domain.com
CORS_ALLOW_METHODS=["GET","POST","OPTIONS","PUT","DELETE"]
CORS_ALLOW_HEADERS=Content-Type,Authorization,X-Request-ID,X-API-Key,Accept,Origin,Cache-Control
ADDITIONAL_ALLOWED_ORIGINS=https://your-other-domain.com
```

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=/api/v1
NEXT_PUBLIC_SITE_URL=https://your-domain.com
NEXT_PUBLIC_WEBSITE_API_KEY=your-website-key
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

### Production Deployment (DigitalOcean)

### Prerequisites

- DigitalOcean account
- GitHub repository connected to DigitalOcean
- Domain name (optional but recommended)

### Deployment Steps

1. **Fork/clone the repository**
2. **Configure environment variables in DigitalOcean dashboard**:
   - Navigate to the App Platform section
   - Create a new app from your GitHub repository
   - Configure the required environment variables listed below
3. **Deploy using App Platform**:
   - Select the `Dockerfile` in the root directory for deployment
   - Set the run command to `./start.sh`
   - Configure HTTP routes to expose port 3000 for the web interface
4. **Set up SSL certificates**:
   - Enable SSL for your app
   - Choose "Let's Encrypt" for automatic certificate management
5. **Configure domain (if applicable)**:
   - Add your custom domain in the Settings > Domains section
   - Update the DNS records as instructed by DigitalOcean

### Environment Variables for DigitalOcean

Required environment variables for production:

- `API_SECRET_KEY`: API master key (mark as Encrypted)
- `JWT_SECRET_KEY`: JWT signing key (mark as Encrypted)
- `ADMIN_API_KEY`: Admin access key (mark as Encrypted)
- `WEBSITE_API_KEY`: Website access key (mark as Encrypted)
- `NODE_ENV`: Set to 'production'
- `NEXT_PUBLIC_API_URL`: Set to '/api/v1' for relative path
- `NEXT_PUBLIC_SITE_URL`: Set to '${\_self.PUBLIC_URL}' to use the app's URL
- `CORS_ALLOW_METHODS`: Set to '["GET","POST","OPTIONS","PUT","DELETE"]' (as a JSON array)
- `FRONTEND_URL`: Set to '${\_self.PUBLIC_URL}' to use the app's URL
- `REQUIRE_API_KEY`: Set to 'true'

### Monitoring

- Access logs through DigitalOcean dashboard
- Monitor resource usage and scaling
- Set up alerts for critical events

## Deployment Troubleshooting

### Common Issues and Solutions

1. **CORS Errors**:

   - Ensure `CORS_ALLOW_METHODS` is formatted as a proper JSON array: `["GET","POST","OPTIONS","PUT","DELETE"]`
   - Add your domain to `ADDITIONAL_ALLOWED_ORIGINS`
   - Check browser console for specific CORS error messages

2. **API Connection Issues**:

   - Ensure `NEXT_PUBLIC_API_URL` is set to `/api/v1` (relative path) in production
   - Verify API keys are correctly set and match between frontend and backend
   - Check the route configuration in `.do/app.yaml` has the correct paths

3. **File Permissions**:

   - Make sure `start.sh` has executable permissions: `chmod +x start.sh`
   - Ensure the downloads directory exists and is writable

4. **Environment Variable Format**:

   - For JSON array values like `CORS_ALLOW_METHODS`, use proper JSON syntax with quotes: `'["GET","POST"]'`
   - For multi-line variables, use appropriate escaping or DigitalOcean's multi-line input

5. **Container Startup Issues**:
   - Check logs in DigitalOcean dashboard
   - Verify that both frontend and backend services start correctly
   - Test the health endpoint after deployment: `curl https://your-app-url/health`

### Debugging Tools

- Use the application logs in DigitalOcean dashboard
- Check browser developer tools for frontend errors
- Test API endpoints directly using curl or Postman
- Verify environment variables are correctly set in the container

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
- API key authentication for all API endpoints
- Dual-key system: admin key and website key
- CORS protection with configurable origins
- File size limits
- Download retention policies
- SSL/TLS encryption
- Trusted proxy configuration

## API Authentication

The API uses a robust two-tier API key authentication system to secure all endpoints. This system ensures that only authorized clients can access the API while maintaining different levels of access control.

### Authentication System

1. **API Key Types**:
   - **Admin Key**: Full access to all endpoints, including protected administrative routes
   - **Website Key**: Standard access for frontend client operations
2. **Implementation Details**:
   - API keys must be included in all requests via the `X-API-Key` header
   - CORS preflight (OPTIONS) requests are automatically handled
   - Development mode can bypass authentication for easier local development
   - Keys are validated against environment variables

### Request Headers

For authenticated requests, include:

```http
X-API-Key: your-api-key-here
```

### Security Features

- **Mandatory Authentication**: All endpoints require valid API keys (except health checks and documentation)
- **Environment-Aware**:
  - Production: Strict API key validation
  - Development: Optional authentication bypass
- **CORS Protection**:
  - Preflight requests handled automatically
  - Configurable allowed origins
  - Secure header validation
- **Error Handling**:
  - Clear 401 Unauthorized responses for invalid/missing keys
  - Detailed error messages in development
  - Generic security responses in production

### Configuration

1. **Environment Variables**:

   ```env
   # Backend (.env)
   API_SECRET_KEY=your-secret-key
   ADMIN_API_KEY=your-admin-key
   WEBSITE_API_KEY=your-website-key
   API_KEY_HEADER_NAME=X-API-Key
   REQUIRE_API_KEY=true

   # Frontend (.env.local)
   NEXT_PUBLIC_WEBSITE_API_KEY=your-website-key
   ```

2. **Development Mode**:
   - Set `REQUIRE_API_KEY=false` for local development
   - API key validation is bypassed when disabled
   - Warning logs indicate when authentication is bypassed

### Implementation Notes

- Frontend automatically includes API key in all requests
- WebSocket connections require valid API keys
- Rate limiting is tied to API key tiers
- Keys are validated before processing any request
- Middleware handles authentication across all routes

### Best Practices

1. **Key Management**:

   - Rotate API keys regularly
   - Use different keys for different environments
   - Never expose admin keys in frontend code
   - Store keys securely in environment variables

2. **Security Recommendations**:
   - Enable SSL/TLS in production
   - Monitor failed authentication attempts
   - Implement key expiration if needed
   - Regular security audits

## Progress Tracking System

The application features a comprehensive progress tracking system:

### Frontend Components

- **SimpleDownloadProgress**: Lightweight progress indicator for video previews

  - Shows download percentage
  - Status icons for downloading, completion, and errors
  - Dark mode support
  - Error message display

- **ProcessingProgress**: Multi-stage progress indicator
  - Analyzing stage (33%)
  - Downloading stage (66%)
  - Processing stage (90%)
  - Real-time status updates
  - Animated loading indicators

### Backend Implementation

- WebSocket-based real-time updates
- Progress tracking for both single and batch downloads
- Automatic status management:
  - Pending: Initial request state
  - Processing: Active download
  - Completed: Successful download
  - Error: Failed download
  - Expired: Download link timeout

### Features

- Automatic file cleanup tracking
- Download expiration countdown
- Batch download progress tracking
- Error handling with detailed messages
- Rate limit quota display
- Dark mode support for all progress elements

### Progress States

1. **Analyzing** (33%): Initial URL verification and metadata extraction
2. **Downloading** (66%): Active video download
3. **Processing** (90%): Final video processing and optimization
4. **Completion** (100%): Download ready for access

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
├── .do/                  # DigitalOcean configuration
│   └── app.yaml          # App Platform config
├── downloads/            # Downloaded videos
├── docker-compose.yml    # Docker Compose config
├── Dockerfile            # Combined deployment Dockerfile
├── start.sh              # Startup script for combined deployment
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
