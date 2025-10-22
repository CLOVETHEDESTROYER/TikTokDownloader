# Social Media Video Downloader

A modern web application for downloading videos from multiple social media platforms, built with FastAPI and Next.js.

## 🚀 Features

- **Video Downloads**

  - TikTok videos without watermark
  - Instagram posts, reels, and stories
  - YouTube videos and Shorts
  - Facebook videos and Reels
  - Support for carousel posts
  - High-quality video processing
  - Automatic file naming and organization

- **Modern Web Interface**

  - Clean, responsive design
  - Real-time progress updates
  - Dark mode support
  - Preview before download
  - Mobile-friendly layout

- **Social Media Automation**

  - Connect Instagram, TikTok, and Facebook accounts
  - Monitor saved and liked posts
  - Automatic content collection
  - Cross-platform publishing to TikTok and Instagram
  - Scheduled posting with custom captions and hashtags
  - Automatic file cleanup after publishing

- **Advanced Features**
  - Rate limiting tiers (Free/Premium/Enterprise)
  - WebSocket progress tracking
  - Automatic file cleanup
  - CSV export option
  - Prometheus metrics
  - Priority-based download queue
  - Real-time publishing status tracking

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

### Docker Deployment

The recommended way to deploy the application is using Docker:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/TikTokDownloader.git
   cd TikTokDownloader
   ```

2. **Configure environment variables:**
   Create a `.env` file in the project root with the following variables:

   ```
   ADMIN_API_KEY=your_admin_key
   API_SECRET_KEY=your_api_secret
   WEBSITE_API_KEY=your_website_key
   ```

3. **Build and start the containers:**

   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

### DigitalOcean App Platform

This project is configured for automatic deployment to DigitalOcean App Platform through GitHub.

1. **Fork this repository** on GitHub
2. **Create a new App on DigitalOcean App Platform**:

   - Go to your DigitalOcean dashboard
   - Click on "Apps" in the left sidebar
   - Click "Create App"
   - Select "GitHub" as your repository source
   - Connect your GitHub account if not already connected
   - Select your forked repository

3. **Configure the application**:

   - The app.yaml file in the .do folder will be automatically detected
   - This provides the default configuration for your services

4. **Set up required secrets**:

   - `API_SECRET_KEY`: Your API secret key
   - `WEBSITE_API_KEY`: Your website API key
   - `ADMIN_API_KEY`: Your admin API key
   - `JWT_SECRET_KEY`: Your JWT secret key

5. **Deploy the application**:
   - Click "Next" and review your app configuration
   - Click "Create Resources" to deploy

The app will now be deployed to DigitalOcean. Every push to the main branch will trigger a new deployment automatically.

### Setting up GitHub Actions (Optional)

For more control over the deployment process, this repository includes a GitHub Actions workflow:

1. **Set up GitHub Secrets**:

   - Go to your repository Settings > Secrets and variables > Actions
   - Add these secrets:
     - `DIGITALOCEAN_ACCESS_TOKEN`: Your DigitalOcean API token
     - `DIGITALOCEAN_APP_ID`: Your DigitalOcean App ID

2. **The workflow will automatically**:
   - Run on pushes to the main branch
   - Use the DigitalOcean CLI tool to trigger deployments
   - Log deployment status

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
- `DOWNLOAD_NO_WATERMARK`: Set to "true" to enable enhanced watermark removal for TikTok videos

## 📡 API Endpoints

### TikTok Endpoints

- `POST /api/v1/tiktok/download`: Download single video
- `POST /api/v1/tiktok/batch`: Download multiple videos
- `GET /api/v1/tiktok/status/{session_id}`: Check download status

### Instagram Endpoints

- `POST /api/v1/instagram/download`: Download Instagram content
- `POST /api/v1/instagram/batch`: Batch download
- Supports posts, reels, and stories

### YouTube Endpoints

- `POST /api/v1/youtube/download`: Download YouTube videos/Shorts
- `POST /api/v1/youtube/download-advanced`: Download with advanced options
- `POST /api/v1/youtube/batch`: Batch download YouTube content
- `POST /api/v1/youtube/batch-advanced`: Batch download with advanced options
- `GET /api/v1/youtube/status/{session_id}`: Check download status
- `GET /api/v1/youtube/shorts-info/{video_id}`: Get Shorts information

### Facebook Endpoints

- `POST /api/v1/facebook/download`: Download Facebook videos
- `POST /api/v1/facebook/download-advanced`: Download with advanced options
- `POST /api/v1/facebook/batch`: Batch download Facebook content
- `POST /api/v1/facebook/batch-advanced`: Batch download with advanced options
- `GET /api/v1/facebook/status/{session_id}`: Check download status
- `GET /api/v1/facebook/reel-info/{video_id}`: Get Reel information

### Audio Extraction Endpoints

- `POST /api/v1/audio/extract`: Extract audio from any platform video
  - Request body: `{"url": "https://..."}`
  - Returns: M4A audio file
  - Supports: TikTok, Facebook, Instagram, YouTube, YouTube Shorts
- `POST /api/v1/audio/batch-extract`: Extract audio from multiple videos
  - Request body: `{"urls": ["https://...", "https://..."]}`
  - Returns: Array of audio extraction results
  - Auto-detects platform from URL
  - Uses FFmpeg for reliable audio extraction

### Social Media Management Endpoints

- `GET /api/v1/social/instagram/oauth/authorize`: Get Instagram OAuth URL
- `POST /api/v1/social/instagram/oauth/callback`: Handle Instagram OAuth callback
- `GET /api/v1/social/accounts`: List connected social accounts
- `POST /api/v1/social/content/collect`: Collect content from accounts
- `GET /api/v1/social/content`: List collected content items
- `POST /api/v1/social/content/{content_id}/download`: Add content to download queue
- `GET /api/v1/social/download-queue/status`: Get download queue status

### Publishing Endpoints

- `POST /api/v1/publishing/schedule`: Schedule a post for future publishing
- `POST /api/v1/publishing/publish-now`: Publish content immediately
- `GET /api/v1/publishing/scheduled-posts`: List scheduled posts
- `GET /api/v1/publishing/scheduled-posts/{id}`: Get specific scheduled post
- `DELETE /api/v1/publishing/scheduled-posts/{id}`: Cancel scheduled post
- `GET /api/v1/publishing/status/{content_id}`: Get publishing status
- `POST /api/v1/publishing/delete-published`: Delete published content
- `POST /api/v1/publishing/cleanup/{content_id}`: Clean up files after publishing
- `GET /api/v1/publishing/platforms`: Get supported publishing platforms

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

The TikTok download service uses a sophisticated approach to extract and download videos without watermarks:

1. **Video Extraction:**

   - Uses yt-dlp to extract video information with specialized TikTok options
   - Prioritizes formats marked as "no_watermark" in TikTok's metadata
   - Implements a fallback chain to ensure watermark-free content

2. **Enhanced Watermark Removal:**

   - Uses the `download_without_watermark: true` option in TikTok extractor
   - Employs FFmpeg for post-processing with specialized filters
   - Configurable via the `DOWNLOAD_NO_WATERMARK` environment variable

3. **Quality Selection:**

   - Supports high, medium and low quality presets
   - High quality uses the best available video/audio combination
   - Medium quality caps resolution at 720p
   - Low quality caps resolution at 480p for faster downloads

4. **Docker Integration:**
   - Pre-configured FFmpeg installation in all Docker containers
   - Volume mounting for efficient file management
   - Environment variables for fine-tuned control

For more technical details, see the implementation in `app/api/app/services/tiktok.py`.

## 🛠️ YouTube Shorts Implementation

The YouTube download service provides comprehensive support for both regular YouTube videos and YouTube Shorts:

1. **Automatic Shorts Detection:**

   - Detects YouTube Shorts based on URL patterns (`/shorts/`)
   - Identifies Shorts by video duration (≤60 seconds)
   - Handles both regular YouTube and Shorts URLs seamlessly

2. **Quality Optimization:**

   - High quality: Up to 1080p for optimal Shorts viewing
   - Medium quality: Up to 720p for balanced size/quality
   - Low quality: Up to 480p for faster downloads

3. **Advanced Features:**

   - Metadata extraction (title, author, duration, view count, etc.)
   - Thumbnail URL extraction
   - Content type detection (video vs shorts)
   - Batch download support

4. **API Endpoints:**
   - Standard download endpoints compatible with existing frontend
   - Advanced endpoints with additional metadata and options
   - Dedicated Shorts information endpoint

For more technical details, see the implementation in `app/api/app/services/youtube.py`.

## 🛠️ Facebook Video Implementation

The Facebook download service provides comprehensive support for Facebook videos, Reels, and live content:

1. **Content Type Detection:**

   - Automatically detects Facebook Reels based on URL patterns (`/reel/`)
   - Identifies live videos and stories
   - Handles regular Facebook videos and posts
   - Supports both `facebook.com` and `fb.watch` URLs

2. **Quality Optimization:**

   - High quality: Up to 1080p for optimal viewing
   - Medium quality: Up to 720p for balanced size/quality
   - Low quality: Up to 480p for faster downloads

3. **Advanced Features:**

   - Metadata extraction (title, author, duration, view count, etc.)
   - Thumbnail URL extraction
   - Content type detection (video, reel, live, story, post)
   - Page name extraction for better organization
   - Batch download support

4. **API Endpoints:**

   - Standard download endpoints compatible with existing frontend
   - Advanced endpoints with additional metadata and options
   - Dedicated Reel information endpoint
   - Support for Facebook-specific content types

5. **Important Considerations:**
   - Some Facebook content may require authentication
   - Rate limiting may apply to Facebook downloads
   - Private or restricted content may not be downloadable
   - Facebook's terms of service must be respected

For more technical details, see the implementation in `app/api/app/services/facebook.py`.

## 🛠️ TikTok Watermark Removal in Docker

This project supports automatic TikTok watermark removal when running in Docker. The following features are enabled:

- FFmpeg installed in container for video processing
- Latest yt-dlp version (2025.4.30) for TikTok download support
- DOWNLOAD_NO_WATERMARK environment variable for enhanced watermark removal

### Quick Start with TikTok Docker Container

For users who only want to use the TikTok watermark removal functionality, we provide a simplified Docker setup:

1. **Run the start script**:

   ```bash
   ./start-tiktok-docker.sh
   ```

   This will:

   - Build and start the TikTok-specific Docker container
   - Set up all required components (FFmpeg, yt-dlp)
   - Configure the environment for optimal watermark removal
   - Verify that everything is working correctly

2. **Use the API**:

   Once the container is running, you can remove TikTok watermarks by sending a POST request:

   ```bash
   curl -X POST http://localhost:8001/api/v1/download \
     -H 'Content-Type: application/json' \
     -d '{"url": "https://www.tiktok.com/your-video-url", "platform": "tiktok", "quality": "high"}'
   ```

3. **Download your videos**:

   Downloaded videos will be available in the `downloads` directory with watermarks removed.

### Testing TikTok Watermark Removal

To verify that your Docker setup is correctly configured for TikTok watermark removal:

```bash
./test-docker-tiktok.sh
```

This will run a series of checks to ensure all components are properly installed and configured.

## 🔄 Social Media Automation Workflow

The application now includes a complete social media automation system that allows you to:

### 1. Connect Social Media Accounts

- **Instagram**: OAuth integration with Instagram Basic Display API
- **TikTok**: TikTok for Developers API integration (coming soon)
- **Facebook**: Facebook Graph API integration (coming soon)

### 2. Content Collection

- Monitor saved posts on Instagram
- Track liked content across platforms
- Automatic URL collection and metadata extraction
- Priority-based download queue

### 3. Content Processing

- Download videos without watermarks
- Extract thumbnails and metadata
- Organize content by platform and type
- Quality optimization for each platform

### 4. Cross-Platform Publishing

- **TikTok Publishing**: Post videos with custom captions and hashtags
- **Instagram Publishing**: Share to Instagram Reels and posts
- **Scheduled Posting**: Schedule content for optimal engagement times
- **Batch Publishing**: Publish to multiple platforms simultaneously

### 5. Automation Features

- **Automatic Cleanup**: Delete local files after successful publishing
- **Retry Logic**: Handle failed uploads with automatic retries
- **Status Tracking**: Real-time monitoring of publishing progress
- **Error Handling**: Comprehensive error reporting and recovery

### 6. Web Dashboard

- **Account Management**: Connect and manage social media accounts
- **Content Browser**: View collected content with thumbnails
- **Publishing Interface**: Easy-to-use publishing and scheduling tools
- **Analytics**: Track publishing performance and engagement

### Getting Started with Automation

1. **Set up API credentials** in your `.env` file:

   ```env
   INSTAGRAM_APP_ID=your_instagram_app_id
   INSTAGRAM_APP_SECRET=your_instagram_app_secret
   TIKTOK_APP_ID=your_tiktok_app_id
   TIKTOK_APP_SECRET=your_tiktok_app_secret
   ```

2. **Access the dashboard** at `http://localhost:3000/dashboard`

3. **Connect your accounts** using the OAuth flow

4. **Start collecting content** from your saved/liked posts

5. **Schedule or publish** your content across platforms

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
