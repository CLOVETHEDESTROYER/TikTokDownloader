import os
import yt_dlp
import uuid
import asyncio
import time
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
from ..core.exceptions import DownloadError, VideoNotFoundError
from ..models.download import DownloadStatus, DownloadResponse, Platform, VideoQuality
from ..core.config import settings

class DownloadManager:
    def __init__(self):
        self.active_downloads: Dict[str, Dict[str, Any]] = {}
        self.completed_downloads: List[Dict[str, Any]] = []
        self.download_folder = settings.DOWNLOAD_FOLDER
        self.file_expiry_seconds = 300  # 5 minutes
        self.cleanup_task = None
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure download directory exists"""
        os.makedirs(self.download_folder, exist_ok=True)

    async def start_cleanup_task(self):
        """Start the cleanup task if it's not already running."""
        if self.cleanup_task is None or self.cleanup_task.done():
            self.cleanup_task = asyncio.create_task(self._cleanup_loop())
        return self.cleanup_task

    async def _cleanup_loop(self):
        """Background task to clean up expired files."""
        while True:
            try:
                now = datetime.now()
                for download_info in list(self.completed_downloads):
                    if now - download_info['timestamp'] > timedelta(minutes=5):
                        file_path = os.path.join(self.download_folder, download_info['filename'])
                        try:
                            if os.path.exists(file_path):
                                os.remove(file_path)
                                print(f"Deleted old file: {download_info['filename']}")
                            self.completed_downloads.remove(download_info)
                        except Exception as e:
                            print(f"Error deleting file {download_info['filename']} or removing from list: {e}")
                
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Error in cleanup loop: {str(e)}")
                await asyncio.sleep(60)

    def _get_ydl_opts(self, filename: str) -> dict:
        """Get yt-dlp options with simplified configuration."""
        return {
            'outtmpl': os.path.join(self.download_folder, filename),
            'format': 'mp4',
            'quiet': False,
            'noplaylist': True
        }

    async def create_download(self, url: str, platform: Platform) -> str:
        """Create a new download session"""
        session_id = str(uuid.uuid4())
        self.active_downloads[session_id] = {
            "status": DownloadStatus.PENDING,
            "progress": 0,
            "url": url,
            "platform": platform,
            "error": None,
            "created_at": None
        }
        return session_id

    async def process_download(
        self,
        session_id: str,
        url: str,
        platform: Platform,
        quality: VideoQuality,
        start_time: float
    ) -> DownloadResponse:
        """Process a single download with simplified error handling"""
        if session_id not in self.active_downloads:
            raise ValueError("Invalid session ID")

        try:
            self.active_downloads[session_id]["status"] = DownloadStatus.PROCESSING
            filename = f"{platform.value}_{uuid.uuid4().hex[:8]}.mp4"
            
            # Download the video
            result = await self._download_video(url, filename)
            
            if result['success']:
                # Update active download status
                self.active_downloads[session_id].update({
                    "status": DownloadStatus.COMPLETED,
                    "filename": filename,
                    "title": result['title'],
                    "progress": 100,
                    "created_at": time.time(),
                    "expires_at": time.time() + self.file_expiry_seconds
                })

                # Add to completed downloads
                self.completed_downloads.append({
                    'filename': filename,
                    'title': result['title'],
                    'url': url,
                    'timestamp': datetime.now()
                })

                return DownloadResponse(
                    session_id=session_id,
                    status=DownloadStatus.COMPLETED,
                    progress=100,
                    url=url,
                    filename=filename,
                    expires_at=self.active_downloads[session_id]["expires_at"],
                    title=result['title'],
                    author=result.get('author', 'Unknown'),
                    duration=time.time() - start_time
                )
            else:
                raise DownloadError(url, result['error'])

        except Exception as e:
            self.active_downloads[session_id]["status"] = DownloadStatus.FAILED
            self.active_downloads[session_id]["error"] = str(e)
            raise

    async def _download_video(self, url: str, filename: str) -> Dict[str, Any]:
        """Download video using yt-dlp with simplified configuration"""
        try:
            ydl_opts = self._get_ydl_opts(filename)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return {
                    'filename': filename,
                    'title': info.get('title', 'Unknown'),
                    'author': info.get('uploader', 'Unknown'),
                    'url': url,
                    'success': True
                }
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'success': False
            }

    async def process_batch_download(
        self,
        session_id: str,
        urls: List[str],
        platform: Platform,
        quality: VideoQuality
    ) -> List[Dict[str, Any]]:
        """Process multiple downloads with simplified approach"""
        if session_id not in self.active_downloads:
            raise ValueError("Invalid session ID")

        self.active_downloads[session_id]['status'] = DownloadStatus.PROCESSING
        results = []

        for i, url in enumerate(urls):
            try:
                filename = f"{platform.value}_batch_{uuid.uuid4().hex[:8]}.mp4"
                result = await self._download_video(url, filename)
                
                if result['success']:
                    self.completed_downloads.append({
                        'filename': filename,
                        'title': result['title'],
                        'url': url,
                        'timestamp': datetime.now()
                    })
                
                results.append(result)
                self.active_downloads[session_id]['progress'] = int((i + 1) / len(urls) * 100)

            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e),
                    'success': False
                })

        self.active_downloads[session_id]['status'] = DownloadStatus.COMPLETED
        self.active_downloads[session_id]['progress'] = 100
        self.active_downloads[session_id]['results'] = results

        return results

    async def get_download_status(self, session_id: str) -> Optional[DownloadResponse]:
        """Get the current status of a download"""
        if session_id not in self.active_downloads:
            return None

        download = self.active_downloads[session_id]
        return DownloadResponse(
            session_id=session_id,
            status=download["status"],
            progress=download["progress"],
            url=download["url"],
            filename=download.get("filename"),
            error=download.get("error"),
            expires_at=download.get("expires_at"),
            title=download.get("title", "Unknown"),
            author=download.get("author", "Unknown")
        )

    def get_download_path(self, filename: str) -> str:
        """Get the full path for a downloaded file"""
        return os.path.join(self.download_folder, filename)
