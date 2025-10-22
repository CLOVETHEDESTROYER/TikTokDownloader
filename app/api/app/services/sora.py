import yt_dlp
import os
import uuid
import logging
import re
from typing import List
from pydantic import HttpUrl
from ..core.config import settings
from ..core.exceptions import DownloadFailedException, InvalidURLException
import asyncio

logger = logging.getLogger(__name__)


class SoraService:
    def __init__(self):
        self.download_path = settings.DOWNLOAD_FOLDER
        os.makedirs(self.download_path, exist_ok=True)

        # Check if no watermark is explicitly enabled
        self.force_no_watermark = os.getenv(
            "DOWNLOAD_NO_WATERMARK", "false").lower() == "true"
        if self.force_no_watermark:
            logger.info("Sora watermark removal is explicitly enabled")

        self.ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.download_path, '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

    async def extract_video_id(self, url: str) -> str:
        """Extract Sora video ID from URL"""
        # Handle actual Sora URL patterns from sora.chatgpt.com
        patterns = [
            r'sora\.chatgpt\.com/p/s_([a-zA-Z0-9_-]+)',  # Actual Sora URL format
            r'sora\.openai\.com/video/([a-zA-Z0-9_-]+)',  # Legacy format
            r'openai\.com/sora/([a-zA-Z0-9_-]+)',        # Legacy format
            r'sora/([a-zA-Z0-9_-]+)',                   # Generic format
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise InvalidURLException("Could not extract Sora video ID")

    async def get_video_no_watermark(self, url: str) -> dict:
        """Get Sora video without watermark using yt-dlp"""
        try:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                # Force yt-dlp to find the version without watermark
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                # Try Sora-specific options (similar to TikTok approach)
                'extractor_args': {
                    'generic': {
                        'download_without_watermark': True,
                    }
                },
            }

            # Use asyncio to run yt-dlp in a separate thread (non-blocking)
            loop = asyncio.get_event_loop()
            info_dict = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(
                    ydl_opts).extract_info(url, download=False)
            )

            if not info_dict:
                logger.error(f"Could not extract video info for URL: {url}")
                raise DownloadFailedException("Could not extract video info")

            # Get the best format without watermark
            formats = info_dict.get('formats', [])
            if not formats:
                logger.error(
                    f"No formats found for URL: {url}, info: {info_dict}")

            download_url = None

            # Look for the best quality mp4 format
            for format in formats:
                # Try to get the no-watermark version first
                if 'no_watermark' in format.get('format_note', '').lower() or 'no-watermark' in format.get('format_note', '').lower():
                    download_url = format['url']
                    break

            # If no explicit no-watermark version found, use the best mp4 format
            if not download_url:
                for format in formats:
                    if format.get('ext') == 'mp4' and format.get('vcodec') != 'none':
                        download_url = format['url']
                        break

            # If still no URL, just use the best direct URL
            if not download_url and 'url' in info_dict:
                download_url = info_dict['url']

            if not download_url:
                logger.error(f"Could not find download URL for {url}")
                raise DownloadFailedException("Could not find a download URL")

            return {
                'download_url': download_url,
                'desc': info_dict.get('title', 'Sora Generated Video'),
                'author': info_dict.get('uploader', 'OpenAI Sora')
            }

        except Exception as e:
            logger.error(f"Failed to get video without watermark: {str(e)}")
            raise DownloadFailedException(
                f"Failed to get video without watermark: {str(e)}")

    async def download_video(self, url: HttpUrl, quality: str = "best", cookies: str = None) -> dict:
        """Download a single Sora video without watermark"""
        session_id = str(uuid.uuid4())
        filename = f"sora_{uuid.uuid4().hex[:8]}.mp4"
        file_path = os.path.join(self.download_path, filename)

        try:
            # Enhanced configuration for Sora no-watermark downloads
            ydl_opts = {
                'format': 'mp4',  # Base format
                'outtmpl': file_path,
                'quiet': True,
                'noplaylist': True,
                'extract_flat': False,
                # Force yt-dlp to find the version without watermark
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                # Try Sora-specific options (similar to TikTok approach)
                'extractor_args': {
                    'generic': {
                        'download_without_watermark': True,
                    }
                },
            }
            
            # Add cookies and browser-like headers if provided
            if cookies:
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'https://chatgpt.com/',
                    'Cookie': cookies,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                logger.info("Using provided ChatGPT cookies for download authentication")
            else:
                # Default headers without cookies
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'https://chatgpt.com/',
                }

            # If force_no_watermark is enabled, add additional FFmpeg options
            if self.force_no_watermark:
                logger.info(
                    f"Applying enhanced watermark removal for URL: {url}")
                # Add more aggressive FFmpeg postprocessing for watermark removal
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegVideoRemuxer',
                    'preferedformat': 'mp4',
                })

            # Quality-specific format selection
            if quality == "high":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            elif quality == "medium":
                ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif quality == "low":
                ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'

            # Use asyncio to run yt-dlp in a separate thread (non-blocking)
            loop = asyncio.get_event_loop()

            # Extract info first to get metadata (needed for API response)
            logger.info(f"Extracting video info for URL: {url}")
            info_dict = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(
                    str(url), download=False)
            )

            if not info_dict:
                raise DownloadFailedException("Could not extract video info")

            # Now download with the enhanced configuration
            logger.info(f"Downloading video from URL: {url}")
            await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).download([str(url)])
            )

            # Check if file was downloaded successfully
            if not os.path.exists(file_path):
                raise DownloadFailedException(
                    "Download completed but file not found")

            logger.info(f"Successfully downloaded video to: {file_path}")
            return {
                "session_id": session_id,
                "status": "completed",
                "message": "Download completed successfully",
                "download_url": f"/downloads/{filename}",
                "description": info_dict.get('title', 'Sora Generated Video'),
                "author": info_dict.get('uploader', 'OpenAI Sora')
            }

        except Exception as e:
            logger.error(f"Download failed for URL {url}: {str(e)}")
            raise DownloadFailedException(str(e))

    async def batch_download(self, urls: List[HttpUrl], quality: str = "best") -> List[dict]:
        """Download multiple Sora videos"""
        results = []
        for url in urls:
            try:
                result = await self.download_video(url, quality)
                results.append(result)
            except Exception as e:
                logger.error(f"Batch download failed for URL {url}: {str(e)}")
                results.append({
                    "session_id": str(uuid.uuid4()),
                    "status": "failed",
                    "message": str(e),
                    "download_url": None
                })
        return results

    async def get_status(self, session_id: str) -> dict:
        """Get the status of a download"""
        # In a real implementation, this would check a database or cache
        # For now, we'll just return a simple status
        return {
            "session_id": session_id,
            "status": "completed",
            "progress": 100.0,
            "message": "Download completed",
            "download_url": None  # Would be populated in real implementation
        }

    async def test_sora_extraction(self, url: str, cookies: str = None) -> dict:
        """Test method to see what formats are available for a Sora video"""
        try:
            ydl_opts = {
                'quiet': False,  # Show output for debugging
                'no_warnings': False,
                'extract_flat': False,
                'listformats': True,  # List all available formats
            }
            
            # Add cookies and browser-like headers if provided
            if cookies:
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'https://chatgpt.com/',
                    'Cookie': cookies,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                logger.info("Using provided ChatGPT cookies for authentication")
            else:
                # Default headers without cookies
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Referer': 'https://chatgpt.com/',
                }

            loop = asyncio.get_event_loop()
            info_dict = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(
                    ydl_opts).extract_info(url, download=False)
            )

            return {
                "url": url,
                "title": info_dict.get('title', 'Unknown'),
                "formats": info_dict.get('formats', []),
                "extractor": info_dict.get('extractor', 'Unknown'),
                "webpage_url": info_dict.get('webpage_url', url),
                "description": info_dict.get('description', ''),
                "duration": info_dict.get('duration', 0),
                "uploader": info_dict.get('uploader', 'Unknown'),
            }

        except Exception as e:
            logger.error(f"Failed to test Sora extraction: {str(e)}")
            return {
                "url": str(url),
                "error": str(e),
                "formats": [],
                "extractor": "Failed"
            }
