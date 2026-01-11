import yt_dlp
import os
import uuid
import asyncio
import logging
import re
import time
from typing import List, Dict, Any
from pydantic import HttpUrl
from ..core.config import settings
from ..core.exceptions import DownloadFailedException, InvalidURLException
from ..models.facebook import (
    FacebookDownloadRequest,
    FacebookDownloadResponse,
    FacebookMediaMetadata,
    FacebookContentType,
    FacebookQuality
)

logger = logging.getLogger(__name__)


class FacebookService:
    def __init__(self):
        self.download_path = settings.DOWNLOAD_FOLDER
        os.makedirs(self.download_path, exist_ok=True)

    def _is_facebook_reel(self, url: str, info: Dict[str, Any]) -> bool:
        """Detect if the URL is a Facebook Reel"""
        url_lower = url.lower()

        # Check URL patterns for Reels
        reel_patterns = [
            r'facebook\.com/reel/',
            r'fb\.watch/.*reel',
            r'facebook\.com/.*/reels/'
        ]

        for pattern in reel_patterns:
            if re.search(pattern, url_lower):
                return True

        # Check if it's marked as a reel in metadata
        if info.get('description', '').lower().find('reel') != -1:
            return True

        return False

    def _determine_content_type(self, url: str, info: Dict[str, Any]) -> FacebookContentType:
        """Determine the type of Facebook content"""
        if self._is_facebook_reel(url, info):
            return FacebookContentType.REEL
        elif info.get('is_live'):
            return FacebookContentType.LIVE
        elif 'story' in url.lower():
            return FacebookContentType.STORY
        else:
            return FacebookContentType.VIDEO

    def _get_format_for_quality(self, quality: FacebookQuality) -> str:
        """Get yt-dlp format string based on quality"""
        quality_map = {
            FacebookQuality.HIGH: 'best[height<=1080]/bestvideo[height<=1080]+bestaudio/best',
            FacebookQuality.MEDIUM: 'best[height<=720]/bestvideo[height<=720]+bestaudio/best',
            FacebookQuality.LOW: 'best[height<=480]/bestvideo[height<=480]+bestaudio/best'
        }
        return quality_map.get(quality, 'best/bestvideo+bestaudio')

    def _extract_metadata(self, info: Dict[str, Any], is_live: bool) -> FacebookMediaMetadata:
        """Extract metadata from Facebook video info"""
        return FacebookMediaMetadata(
            title=info.get('title', ''),
            author=info.get('uploader', ''),
            duration=info.get('duration', 0),
            view_count=info.get('view_count', 0),
            like_count=info.get('like_count', 0),
            description=info.get('description', ''),
            upload_date=info.get('upload_date', ''),
            content_type=FacebookContentType.VIDEO,
            is_live=is_live,
            thumbnail_url=info.get('thumbnail', ''),
            page_name=info.get('uploader', '')
        )

    async def download_video(self, url: HttpUrl, quality: str = "high") -> dict:
        """Download a Facebook video"""
        session_id = str(uuid.uuid4())
        filename = f"facebook_{uuid.uuid4().hex[:8]}.mp4"
        file_path = os.path.join(self.download_path, filename)

        try:
            # Quality mapping - handle 'best' as 'high'
            quality_str = quality.lower()
            if quality_str == 'best':
                quality_str = 'high'
            quality_enum = FacebookQuality(quality_str)
            format_string = self._get_format_for_quality(quality_enum)

            ydl_opts = {
                'format': format_string,
                'outtmpl': file_path,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'socket_timeout': 60,
                'retries': 5,
                # Facebook-specific options for better compatibility
                'writethumbnail': False,
                'writeinfojson': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                # Better user agent for Facebook
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'referer': 'https://www.facebook.com/',
                # Handle Facebook share URLs better
                'noplaylist': True,
                'ignoreerrors': False,
                # Add post-processing options to ensure video+audio merging with Apple compatibility
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                # Force Apple-compatible codecs via FFmpeg options
                'ffmpeg_location': None,  # Use system FFmpeg
                'postprocessor_args': {
                    'ffmpeg': [
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-profile:v', 'high',
                        '-level', '4.0',
                        '-movflags', '+faststart',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'medium',
                        '-crf', '23'
                    ]
                },
                # Facebook may require cookies for some content
                'cookiefile': None,  # Can be configured if needed
            }

            # Use asyncio to run yt-dlp in a separate thread (non-blocking)
            loop = asyncio.get_event_loop()

            # Extract info first to get metadata
            logger.info(f"Extracting Facebook video info for URL: {url}")
            info_dict = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(
                    str(url), download=False)
            )

            if not info_dict:
                raise DownloadFailedException(
                    "Could not extract Facebook video info")

            # Check if it's a live video
            is_live = info_dict.get('is_live', False)
            content_type = self._determine_content_type(str(url), info_dict)

            # Now download with the configuration
            logger.info(
                f"Downloading Facebook {'Reel' if content_type == FacebookContentType.REEL else 'video'} from URL: {url}")
            await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).download([str(url)])
            )

            # Check if file was downloaded successfully
            if not os.path.exists(file_path):
                raise DownloadFailedException(
                    "Download completed but file not found")

            # Update file timestamp to current time for better organization on mobile devices
            current_time = time.time()
            os.utime(file_path, (current_time, current_time))
            logger.info(f"Updated file timestamp to current time for: {file_path}")

            logger.info(
                f"Successfully downloaded Facebook video to: {file_path}")

            # Extract metadata
            metadata = self._extract_metadata(info_dict, is_live)

            return {
                "session_id": session_id,
                "status": "completed",
                "message": f"Facebook {'Reel' if content_type == FacebookContentType.REEL else 'video'} downloaded successfully",
                "download_url": f"/downloads/{filename}",
                "title": info_dict.get('title', ''),
                "author": info_dict.get('uploader', 'unknown'),
                "duration": info_dict.get('duration', 0),
                "is_live": is_live,
                "content_type": content_type.value,
                "metadata": metadata.dict()
            }

        except Exception as e:
            logger.error(f"Facebook download failed for URL {url}: {str(e)}")
            raise DownloadFailedException(str(e))

    async def batch_download(self, urls: List[HttpUrl], quality: str = "high") -> List[dict]:
        """Download multiple Facebook videos"""
        results = []

        for url in urls:
            try:
                result = await self.download_video(url, quality)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to download {url}: {str(e)}")
                # Include all required fields for DownloadResponse
                results.append({
                    "session_id": str(uuid.uuid4()),
                    "status": "failed",
                    "message": f"Download failed: {str(e)}",
                    "url": str(url),
                    "error": str(e),
                    "progress": 0
                })

        return results

    async def get_status(self, session_id: str) -> dict:
        """Get download status by session ID"""
        return {
            "session_id": session_id,
            "status": "completed",
            "progress": 100
        }
