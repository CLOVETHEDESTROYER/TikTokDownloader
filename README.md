# TikTok and Instagram Downloader

A modern web application for downloading TikTok and Instagram content, built with FastAPI and Next.js.

## 🚀 Features

- **Video Downloads**

  - TikTok videos without watermark
  - Instagram posts, reels, and stories
  - Support for carousel posts
  - High-quality video processing
  - Automatic file naming and organization

- **Modern Web Interface**

  - Clean, responsive design
  - Real-time progress updates
  - Dark mode support
  - Preview before download
  - Mobile-friendly layout

- **Advanced Features**
  - Rate limiting tiers (Free/Premium/Enterprise)
  - WebSocket progress tracking
  - Automatic file cleanup
  - CSV export option
  - Prometheus metrics

## 📁 Project Structure

```
tiktok-downloader/
├── app/                    # Main application code
│   ├── api/               # FastAPI backend
│   │   ├── app/          # API application
│   │   │   ├── routes/   # API endpoints
│   │   │   ├── services/ # Business logic
│   │   │   ├── models/   # Data models
│   │   │   └── core/     # Core functionality
│   │   ├── downloads/    # Downloaded files
│   │   └── logs/        # Application logs
│   └── web/              # Next.js frontend
│       ├── src/         # React components
│       └── public/      # Static assets
├── scripts/              # Utility scripts
├── config/              # Configuration files
└── tests/              # Test suite
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- FFmpeg

### Local Development

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/TikTokDownloader.git
   cd TikTokDownloader
   ```

2. **Set up the backend**:

   ```bash
   cd app/api
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

3. **Set up the frontend**:

   ```bash
   cd ../web
   npm install
   ```

4. **Configure environment**:

   ```bash
   # Backend (.env in app/api)
   API_SECRET_KEY=your-secret
   WEBSITE_API_KEY=your-key
   DOWNLOAD_FOLDER=downloads
   FRONTEND_URL=http://localhost:3000

   # Frontend (.env.local in app/web)
   NEXT_PUBLIC_API_URL=/api/v1
   NEXT_PUBLIC_WEBSITE_API_KEY=your-key
   ```

5. **Start development servers**:

   ```bash
   # Terminal 1 (Backend)
   cd app/api
   uvicorn app.main:app --reload

   # Terminal 2 (Frontend)
   cd app/web
   npm run dev
   ```

## 🚀 Deployment

### DigitalOcean App Platform

1. Fork this repository
2. Create a new app in DigitalOcean App Platform
3. Connect your forked repository
4. Configure environment variables
5. Deploy!

### Environment Variables

#### Required Variables

- `API_SECRET_KEY`: API master key
- `WEBSITE_API_KEY`: Frontend access key
- `DOWNLOAD_FOLDER`: Path for downloads
- `FRONTEND_URL`: Your domain

#### Optional Features

- `ENABLE_METRICS`: Enable Prometheus metrics
- `RATE_LIMIT_PER_MINUTE`: Custom rate limits
- `DOWNLOAD_EXPIRY_MINUTES`: File cleanup timing

## 📡 API Endpoints

### TikTok Endpoints

- `POST /api/v1/tiktok/download`: Download single video
- `POST /api/v1/tiktok/batch`: Download multiple videos
- `GET /api/v1/tiktok/status/{session_id}`: Check download status

### Instagram Endpoints

- `POST /api/v1/instagram/download`: Download Instagram content
- `POST /api/v1/instagram/batch`: Batch download
- Supports posts, reels, and stories

### Utility Endpoints

- `GET /api/v1/quota`: Check rate limit quota
- `GET /health`: Service health check
- `GET /metrics`: Prometheus metrics (protected)

## 🔒 Security Features

- API key authentication
- Rate limiting by IP and tier
- Secure file handling
- CORS protection
- Request validation

## 📊 Monitoring

- Download success/failure metrics
- Rate limit tracking
- System resource utilization
- Real-time WebSocket stats

## 💾 Database Schema

This application does not use a persistent database. Instead, it uses in-memory storage in the form of dictionaries to track:

- Active downloads: `{session_id: download_metadata}`
- Rate limits: `{ip: quota_usage}`

All downloaded files are stored in the filesystem in the configured `DOWNLOAD_FOLDER`. Files are automatically cleaned up after a configurable expiry period.

## 🛠️ TikTok Downloader Implementation

The TikTok download service uses yt-dlp to extract and download videos without watermarks:

1. Video extraction (`get_video_no_watermark`):

   - Uses yt-dlp to extract video information
   - Looks for formats marked as "no_watermark"
   - Falls back to the best mp4 format available

2. Download process:
   - Direct download through yt-dlp
   - Uses FFmpeg post-processing to ensure watermarks are removed
   - Creates a unique filename for each download

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational purposes only. Respect copyright and terms of service when downloading content.

---
