import yt_dlp
import os
import uuid
import asyncio
import logging
import re
from typing import List, Dict, Any
from pydantic import HttpUrl
from ..core.config import settings
from ..core.exceptions import DownloadFailedException, InvalidURLException
from ..models.youtube import (
    YouTubeDownloadRequest, 
    YouTubeDownloadResponse, 
    YouTubeMediaMetadata,
    YouTubeContentType,
    YouTubeQuality
)

logger = logging.getLogger(__name__)


class YouTubeService:
    def __init__(self):
        self.download_path = settings.DOWNLOAD_FOLDER
        os.makedirs(self.download_path, exist_ok=True)

    def _is_youtube_shorts(self, url: str, info: Dict[str, Any]) -> bool:
        """Detect if the URL is a YouTube Shorts video"""
        url_lower = url.lower()
        
        # Check URL patterns for Shorts
        shorts_patterns = [
            r'youtube\.com/shorts/',
            r'youtube\.com/watch\?v=.*&.*shorts',
            r'youtu\.be/.*\?.*shorts'
        ]
        
        for pattern in shorts_patterns:
            if re.search(pattern, url_lower):
                return True
        
        # Check video duration (Shorts are typically 60 seconds or less)
        duration = info.get('duration', 0)
        if duration and duration <= 60:
            return True
            
        # Check if the video is marked as Shorts in metadata
        if info.get('is_live') is False and duration and duration <= 60:
            return True
            
        return False

    def _determine_content_type(self, url: str, info: Dict[str, Any]) -> YouTubeContentType:
        """Determine the type of YouTube content"""
        if self._is_youtube_shorts(url, info):
            return YouTubeContentType.SHORTS
        elif info.get('is_live'):
            return YouTubeContentType.LIVE
        elif info.get('_type') == 'playlist':
            return YouTubeContentType.PLAYLIST
        else:
            return YouTubeContentType.VIDEO

    def _get_format_for_quality(self, quality: YouTubeQuality) -> str:
        """Get yt-dlp format string based on quality"""
        quality_map = {
            YouTubeQuality.HIGH: 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            YouTubeQuality.MEDIUM: 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            YouTubeQuality.LOW: 'bestvideo[height<=480]+bestaudio/best[height<=480]'
        }
        return quality_map.get(quality, 'bestvideo+bestaudio/best')

    def _extract_metadata(self, info: Dict[str, Any], is_shorts: bool) -> YouTubeMediaMetadata:
        """Extract metadata from YouTube video info"""
        return YouTubeMediaMetadata(
            title=info.get('title', ''),
            author=info.get('uploader', ''),
            duration=info.get('duration', 0),
            view_count=info.get('view_count', 0),
            like_count=info.get('like_count', 0),
            description=info.get('description', ''),
            upload_date=info.get('upload_date', ''),
            content_type=YouTubeContentType.SHORTS if is_shorts else YouTubeContentType.VIDEO,
            is_shorts=is_shorts,
            thumbnail_url=info.get('thumbnail', '')
        )

    async def download_video(self, url: HttpUrl, quality: str = "high") -> dict:
        """Download a YouTube video or Short"""
        session_id = str(uuid.uuid4())
        filename = f"youtube_{uuid.uuid4().hex[:8]}.mp4"
        file_path = os.path.join(self.download_path, filename)

        try:
            # Quality mapping
            quality_enum = YouTubeQuality(quality.lower())
            format_string = self._get_format_for_quality(quality_enum)

            ydl_opts = {
                'format': format_string,
                'outtmpl': file_path,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'socket_timeout': 30,
                'retries': 3,
                # YouTube-specific options
                'extract_flat': False,
                'writethumbnail': False,
                'writeinfojson': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
            }

            # Use asyncio to run yt-dlp in a separate thread (non-blocking)
            loop = asyncio.get_event_loop()

            # Extract info first to get metadata
            logger.info(f"Extracting YouTube video info for URL: {url}")
            info_dict = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(
                    str(url), download=False)
            )

            if not info_dict:
                raise DownloadFailedException("Could not extract YouTube video info")

            # Check if it's a Shorts video
            is_shorts = self._is_youtube_shorts(str(url), info_dict)
            content_type = self._determine_content_type(str(url), info_dict)

            # Now download with the configuration
            logger.info(f"Downloading YouTube {'Shorts' if is_shorts else 'video'} from URL: {url}")
            await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).download([str(url)])
            )

            # Check if file was downloaded successfully
            if not os.path.exists(file_path):
                raise DownloadFailedException("Download completed but file not found")

            logger.info(f"Successfully downloaded YouTube {'Shorts' if is_shorts else 'video'} to: {file_path}")
            
            # Extract metadata
            metadata = self._extract_metadata(info_dict, is_shorts)
            
            return {
                "session_id": session_id,
                "status": "completed",
                "message": f"YouTube {'Shorts' if is_shorts else 'video'} downloaded successfully",
                "download_url": f"/downloads/{filename}",
                "title": info_dict.get('title', ''),
                "author": info_dict.get('uploader', 'unknown'),
                "duration": info_dict.get('duration', 0),
                "is_shorts": is_shorts,
                "content_type": content_type.value,
                "metadata": metadata.dict()
            }

        except Exception as e:
            logger.error(f"YouTube download failed for URL {url}: {str(e)}")
            raise DownloadFailedException(str(e))

    async def batch_download(self, urls: List[HttpUrl], quality: str = "high") -> List[dict]:
        """Download multiple YouTube videos/Shorts"""
        results = []
        
        for url in urls:
            try:
                result = await self.download_video(url, quality)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to download {url}: {str(e)}")
                results.append({
                    "url": str(url),
                    "status": "failed",
                    "error": str(e)
                })
        
        return results

    async def get_status(self, session_id: str) -> dict:
        """Get download status by session ID"""
        # This would typically check against active downloads
        # For now, return a basic status
        return {
            "session_id": session_id,
            "status": "completed",
            "progress": 100
        }
