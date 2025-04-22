import os
import yt_dlp
import uuid
import asyncio
import time
from typing import Dict, Optional, List, Any
from concurrent.futures import ThreadPoolExecutor
from ..core.exceptions import (
    DownloadError,
    VideoNotFoundError,
    QualityNotAvailableError,
    NetworkError
)
from ..models.download import (
    DownloadStatus,
    DownloadResponse,
    Platform,
    VideoQuality,
    BatchDownloadResponse
)


class DownloadManager:
    def __init__(self):
        self.active_downloads: Dict[str, Dict[str, Any]] = {}
        self.download_folder = "downloads"
        self.executor = ThreadPoolExecutor(
            max_workers=5)  # Limit concurrent downloads
        self.file_expiry_seconds = 300  # 5 minutes
        self.cleanup_task = None
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
                current_time = time.time()
                # Check all active downloads
                for session_id, download in list(self.active_downloads.items()):
                    if (
                        download.get("status") == DownloadStatus.COMPLETED
                        and download.get("created_at")
                        and current_time - download["created_at"] >= self.file_expiry_seconds
                    ):
                        await self._cleanup_download(session_id)

                # Sleep for 30 seconds before next check
                await asyncio.sleep(30)
            except Exception as e:
                print(f"Error in cleanup loop: {str(e)}")
                await asyncio.sleep(30)  # Sleep even if there's an error

    async def _cleanup_download(self, session_id: str):
        """Clean up a specific download."""
        try:
            download = self.active_downloads.get(session_id)
            if download and download.get("filename"):
                file_path = os.path.join(
                    self.download_folder, download["filename"])
                if os.path.exists(file_path):
                    os.remove(file_path)
                # Update status to indicate file is no longer available
                download["status"] = DownloadStatus.EXPIRED
                download["file_expired"] = True
        except Exception as e:
            print(f"Error cleaning up download {session_id}: {str(e)}")

    def _get_ydl_opts(self, platform: Platform, quality: VideoQuality, filename: str) -> dict:
        format_opts = {
            VideoQuality.HIGH: 'bestvideo+bestaudio/best',
            VideoQuality.MEDIUM: 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            VideoQuality.LOW: 'bestvideo[height<=480]+bestaudio/best[height<=480]'
        }

        return {
            'format': format_opts[quality],
            'outtmpl': os.path.join(self.download_folder, filename),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': False,  # Changed to False to handle errors properly
            'socket_timeout': 30,
            'retries': 3
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
            "created_at": None  # Will be set when download completes
        }
        return session_id

    async def _extract_video_info(self, url: str, ydl_opts: dict) -> dict:
        """Extract video information asynchronously"""
        try:
            # Modify options to extract thumbnails without downloading
            info_opts = ydl_opts.copy()
            info_opts['extract_flat'] = False
            info_opts['skip_download'] = True

            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                self.executor,
                lambda: yt_dlp.YoutubeDL(
                    info_opts).extract_info(url, download=False)
            )
        except yt_dlp.utils.DownloadError as e:
            if "Video unavailable" in str(e):
                raise VideoNotFoundError(url)
            raise DownloadError(url, str(e))
        except Exception as e:
            raise NetworkError(url, str(e))

    async def _download_video_async(self, url: str, ydl_opts: dict, session_id: str) -> None:
        """Download video asynchronously with progress tracking"""
        try:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if 'total_bytes' in d and d['total_bytes'] > 0:
                        progress = (d['downloaded_bytes'] /
                                    d['total_bytes']) * 100
                        self.active_downloads[session_id]["progress"] = int(
                            progress)
                elif d['status'] == 'finished':
                    self.active_downloads[session_id]["progress"] = 100

            ydl_opts['progress_hooks'] = [progress_hook]

            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                self.executor,
                lambda: yt_dlp.YoutubeDL(ydl_opts).download([url])
            )

        except yt_dlp.utils.DownloadError as e:
            raise DownloadError(url, str(e))
        except Exception as e:
            raise NetworkError(url, str(e))

    async def process_download(
        self,
        session_id: str,
        url: str,
        platform: Platform,
        quality: VideoQuality
    ) -> DownloadResponse:
        """Process a single download with improved error handling"""
        if session_id not in self.active_downloads:
            raise ValueError("Invalid session ID")

        try:
            self.active_downloads[session_id]["status"] = DownloadStatus.PROCESSING
            filename = f"{platform.value}_{uuid.uuid4().hex[:8]}.mp4"

            ydl_opts = self._get_ydl_opts(platform, quality, filename)

            # First, check if video exists and quality is available
            info = await self._extract_video_info(url, ydl_opts)
            if not info:
                raise VideoNotFoundError(url)

            # Extract video metadata
            title = info.get('title', 'Untitled Video')
            author = info.get('uploader', info.get(
                'channel', 'Unknown Creator'))
            duration = info.get('duration')

            # Extract the best thumbnail URL
            thumbnail = None
            if info.get('thumbnails'):
                thumbnails = sorted(
                    [t for t in info.get('thumbnails', []) if t.get('url')],
                    key=lambda t: t.get('preference', 0) +
                    t.get('width', 0)/100,
                    reverse=True
                )
                if thumbnails:
                    thumbnail = thumbnails[0]['url']

            # Save metadata to active_downloads
            self.active_downloads[session_id].update({
                "title": title,
                "author": author,
                "duration": duration,
                "thumbnail": thumbnail
            })

            # Check if requested quality is available
            formats = info.get('formats', [])
            if not any(f for f in formats if self._matches_quality(f, quality)):
                raise QualityNotAvailableError(url, quality.value)

            # Download the video
            await self._download_video_async(url, ydl_opts, session_id)

            # Set completion status and timestamp
            self.active_downloads[session_id].update({
                "status": DownloadStatus.COMPLETED,
                "filename": filename,
                "created_at": time.time(),
                "expires_at": time.time() + self.file_expiry_seconds
            })

            # Prepare download response with additional metadata
            return DownloadResponse(
                session_id=session_id,
                status=DownloadStatus.COMPLETED,
                progress=100,
                url=url,
                filename=filename,
                expires_at=self.active_downloads[session_id]["expires_at"],
                title=title,
                author=author,
                duration=duration,
                thumbnail=thumbnail
            )

        except Exception as e:
            self.active_downloads[session_id]["status"] = DownloadStatus.FAILED
            self.active_downloads[session_id]["error"] = str(e)
            raise

    def _matches_quality(self, format_info: dict, quality: VideoQuality) -> bool:
        """Check if format matches requested quality"""
        height = format_info.get('height', 0)
        if quality == VideoQuality.HIGH:
            return height >= 720
        elif quality == VideoQuality.MEDIUM:
            return 480 <= height <= 720
        else:
            return height <= 480

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
            title=download.get("title"),
            author=download.get("author"),
            duration=download.get("duration"),
            thumbnail=download.get("thumbnail")
        )

    async def process_batch_download(
        self,
        session_id: str,
        urls: List[str],
        platform: Platform,
        quality: VideoQuality
    ) -> BatchDownloadResponse:
        """Process multiple downloads with improved error handling"""
        if session_id not in self.active_downloads:
            raise ValueError("Invalid session ID")

        total_urls = len(urls)
        self.active_downloads[session_id].update({
            "total_urls": total_urls,
            "processed_urls": 0,
            "status": DownloadStatus.PROCESSING,
            "errors": []
        })

        try:
            for i, url in enumerate(urls, 1):
                try:
                    filename = f"{platform.value}_batch_{uuid.uuid4().hex[:8]}.mp4"
                    ydl_opts = self._get_ydl_opts(platform, quality, filename)

                    # Check video availability
                    await self._extract_video_info(url, ydl_opts)

                    # Download video
                    await self._download_video_async(url, ydl_opts, session_id)

                except Exception as e:
                    self.active_downloads[session_id]["errors"].append({
                        "url": url,
                        "error": str(e)
                    })

                self.active_downloads[session_id]["processed_urls"] = i
                self.active_downloads[session_id]["progress"] = int(
                    (i / total_urls) * 100)

            # Set final status based on errors
            has_errors = bool(self.active_downloads[session_id]["errors"])
            final_status = DownloadStatus.COMPLETED if not has_errors else DownloadStatus.FAILED
            self.active_downloads[session_id]["status"] = final_status

            return BatchDownloadResponse(
                session_id=session_id,
                total_urls=total_urls,
                processed_urls=self.active_downloads[session_id]["processed_urls"],
                status=final_status,
                progress=100
            )

        except Exception as e:
            self.active_downloads[session_id]["status"] = DownloadStatus.FAILED
            self.active_downloads[session_id]["error"] = str(e)
            raise
