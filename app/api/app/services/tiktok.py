import yt_dlp
import os
import uuid
import requests
import re
from typing import List
from pydantic import HttpUrl
from ..core.config import settings
from ..core.exceptions import DownloadFailedException, InvalidURLException
import asyncio


class TikTokService:
    def __init__(self):
        self.download_path = settings.DOWNLOAD_FOLDER
        os.makedirs(self.download_path, exist_ok=True)

        self.ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.download_path, '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

    async def extract_video_id(self, url: str) -> str:
        """Extract TikTok video ID from URL"""
        # Handle both share URLs and direct URLs
        patterns = [
            r'video/(\d+)',
            r'v/(\d+)',
            r'/(\d+)?',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise InvalidURLException("Could not extract TikTok video ID")

    async def get_video_no_watermark(self, url: str) -> dict:
        """Get TikTok video without watermark using yt-dlp"""
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
            }

            # Use asyncio to run yt-dlp in a separate thread (non-blocking)
            loop = asyncio.get_event_loop()
            info_dict = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(
                    ydl_opts).extract_info(url, download=False)
            )

            if not info_dict:
                raise DownloadFailedException("Could not extract video info")

            # Get the best format without watermark
            # yt-dlp already prioritizes the no-watermark versions
            formats = info_dict.get('formats', [])
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
                raise DownloadFailedException("Could not find a download URL")

            return {
                'download_url': download_url,
                'desc': info_dict.get('title', ''),
                'author': info_dict.get('uploader', 'unknown')
            }

        except Exception as e:
            raise DownloadFailedException(
                f"Failed to get video without watermark: {str(e)}")

    async def download_video(self, url: HttpUrl, quality: str = "best") -> dict:
        """Download a single TikTok video without watermark"""
        session_id = str(uuid.uuid4())

        try:
            # Get video info and no-watermark URL
            video_info = await self.get_video_no_watermark(str(url))

            # Generate unique filename
            filename = f"tiktok_{uuid.uuid4().hex[:8]}.mp4"
            file_path = os.path.join(self.download_path, filename)

            # Download the video
            response = requests.get(video_info['download_url'], stream=True)
            if response.status_code != 200:
                raise DownloadFailedException("Failed to download video")

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            return {
                "session_id": session_id,
                "status": "completed",
                "message": "Download completed successfully",
                "download_url": f"/downloads/{filename}",
                "description": video_info['desc'],
                "author": video_info['author']
            }

        except Exception as e:
            raise DownloadFailedException(str(e))

    async def batch_download(self, urls: List[HttpUrl], quality: str = "best") -> List[dict]:
        """Download multiple TikTok videos"""
        results = []
        for url in urls:
            try:
                result = await self.download_video(url, quality)
                results.append(result)
            except Exception as e:
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
