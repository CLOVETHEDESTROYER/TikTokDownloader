import yt_dlp
import os
import uuid
import logging
import time
from typing import List
from pydantic import HttpUrl
from ..core.config import settings
from ..core.exceptions import DownloadFailedException, InvalidURLException
import asyncio

logger = logging.getLogger(__name__)


class AudioExtractorService:
    def __init__(self):
        self.download_path = settings.DOWNLOAD_FOLDER

    def _detect_platform(self, url: str) -> str:
        """Auto-detect platform from URL"""
        if 'tiktok.com' in url:
            return 'tiktok'
        elif 'facebook.com' in url or 'fb.watch' in url:
            return 'facebook'
        elif 'instagram.com' in url:
            return 'instagram'
        elif 'youtube.com' in url or 'youtu.be' in url:
            return 'youtube'
        return 'unknown'

    async def extract_audio(self, url: HttpUrl) -> dict:
        """Extract audio from video URL"""
        session_id = str(uuid.uuid4())
        filename = f"audio_{uuid.uuid4().hex[:8]}.m4a"
        file_path = os.path.join(self.download_path, filename)

        try:
            platform = self._detect_platform(str(url))

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': file_path.replace('.m4a', '.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                    'preferredquality': '0',  # Best quality
                }],
                'socket_timeout': 30,
                'retries': 3,
            }

            loop = asyncio.get_event_loop()

            # Extract info and download
            info_dict = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(
                    str(url), download=True)
            )

            if not info_dict:
                raise DownloadFailedException("Could not extract audio")

            # Verify file exists
            if not os.path.exists(file_path):
                raise DownloadFailedException(
                    "Audio extraction completed but file not found")

            # Update file timestamp to current time for better organization on mobile devices
            current_time = time.time()
            os.utime(file_path, (current_time, current_time))
            logger.info(f"Updated audio file timestamp to current time for: {file_path}")

            return {
                "session_id": session_id,
                "status": "completed",
                "message": "Audio extracted successfully",
                "audio_url": f"/downloads/{filename}",
                "title": info_dict.get('title', ''),
                "duration": info_dict.get('duration'),
                "platform": platform
            }

        except Exception as e:
            logger.error(f"Audio extraction failed for URL {url}: {str(e)}")
            return {
                "session_id": session_id,
                "status": "failed",
                "message": f"Audio extraction failed: {str(e)}",
                "audio_url": None,
                "title": None,
                "duration": None,
                "platform": platform
            }

    async def batch_extract_audio(self, urls: List[HttpUrl]) -> List[dict]:
        """Extract audio from multiple video URLs"""
        results = []
        for url in urls:
            result = await self.extract_audio(url)
            results.append(result)
        return results
