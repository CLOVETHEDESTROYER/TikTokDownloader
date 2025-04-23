# TikTok and Instagram Downloader

This project is a comprehensive solution for downloading videos from TikTok and Instagram using Python and the `yt-dlp` library. It includes both backend and frontend components to facilitate video downloading and management.

## Features

- **TikTok Video Downloading**: Download single or multiple TikTok videos, save them in high quality, and automatically name and organize files.
- **Instagram Content Downloading**: Download Instagram posts, reels, and stories, with support for carousel posts and optional authentication for private content.
- **CSV Export**: Export metadata of downloaded content to CSV files.
- **Web Interface**: A Next.js frontend for interacting with the downloader.

## Requirements

- Python 3.x
- Node.js
- `yt-dlp` library
- Optional: Authentication cookies for Instagram private content

## Installation

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

## Usage

### Backend

1. **Run the FastAPI server**:

   ```bash
   uvicorn backend.app.main:app --reload
   ```

2. **Access the API documentation**:
   Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

### Frontend

1. **Run the development server**:

   ```bash
   npm run dev
   ```

2. **Open the application**:
   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Authentication for Instagram

To download private content from Instagram, you need to provide authentication cookies:

1. Log in to Instagram via your browser.
2. Use a browser extension like "EditThisCookie" to export cookies.
3. Save them to `instagram_cookies.txt` in the Netscape cookie format.

## File Structure

- **backend/**: Contains the FastAPI application and services.
- **frontend/**: Contains the Next.js application.
- **downloads/**: Directory where downloaded videos are stored.

## Future Enhancements

- Watermark detection and removal
- Cloud sync options
- GUI with Tkinter
- Telegram bot integration

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or support, please contact [your email].

---
