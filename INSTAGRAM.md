# 📸 Instagram Downloader

This extension to the TikTok downloader allows you to download Instagram posts, reels, and stories using Python and the `yt-dlp` library.

## 🚀 Features

- ✅ Download single or multiple Instagram posts and reels
- ✅ Support for carousel posts (multiple images/videos in one post)
- ✅ CSV export of metadata
- ✅ Optional authentication for private content

## 📝 Usage Instructions

### Authentication (Optional)

For accessing private content or content from accounts you follow, you'll need to provide authentication cookies:

1. Log in to Instagram via your browser
2. Use a browser extension like "EditThisCookie" (Chrome) or "Cookie-Editor" (Firefox) to export cookies
3. Save them to the `instagram_cookies.txt` file in the Netscape cookie format

### Command Line Usage

#### Single Post/Reel Download

```bash
python instagram_downloader.py
```

#### Batch Download

1. Create a text file with Instagram URLs (one per line)
2. Run:

```bash
python batch_instagram_downloader.py
```

### Using the Launcher

1. Run `python launcher.py`
2. Select "Instagram" from the main menu
3. Choose the download option you prefer

## 📋 URL Formats Supported

- Post URLs: `https://www.instagram.com/p/CODE/`
- Reel URLs: `https://www.instagram.com/reel/CODE/`
- Story URLs: `https://www.instagram.com/stories/USERNAME/ID/`

## 🔍 Special Features

### Carousel Posts

Instagram carousel posts (with multiple photos/videos) are automatically detected and all media items will be downloaded.

### Private Content

With proper authentication via cookies, you can download:

- Posts from private accounts you follow
- Stories from accounts you follow

## ⚠️ Limitations

- Instagram's terms of service may change
- Not all content may be accessible
- Rate limiting may occur with excessive usage

## 💡 Tips

- Download your own content as backups
- Respect copyright and privacy when downloading content
- Use the CSV export feature to keep track of downloaded content
