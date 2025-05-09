import yt_dlp
import os
import uuid
import asyncio
import logging
from typing import List
from pydantic import HttpUrl
from ..core.config import settings
from ..core.exceptions import DownloadFailedException, InvalidURLException

logger = logging.getLogger(__name__)


class InstagramService:
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

    async def download_content(self, url: HttpUrl, quality: str = "best") -> dict:
        """Download Instagram content (post, reel, or story)"""
        session_id = str(uuid.uuid4())
        filename = f"instagram_{uuid.uuid4().hex[:8]}"
        file_path = os.path.join(self.download_path, filename)

        try:
            ydl_opts = {
                'format': quality,
                'outtmpl': file_path + '.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'noplaylist': False,  # Allow playlists for carousel posts
                'extract_flat': False,
                'cookiefile': settings.INSTAGRAM_COOKIES_FILE if os.path.exists(settings.INSTAGRAM_COOKIES_FILE) else None,
                'retries': settings.INSTAGRAM_MAX_RETRIES,
                'socket_timeout': settings.INSTAGRAM_TIMEOUT
            }

            # Use asyncio to run yt-dlp in a separate thread (non-blocking)
            loop = asyncio.get_event_loop()

            # Extract info first to get metadata
            info_dict = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(
                    str(url), download=False)
            )

            if not info_dict:
                raise InvalidURLException(
                    "Could not extract Instagram content info")

            # Handle both single posts and carousels
            if '_type' in info_dict and info_dict['_type'] == 'playlist':
                # This is a carousel post
                files = []
                for idx, entry in enumerate(info_dict['entries']):
                    entry_file_path = file_path + f"_{idx}.%(ext)s"
                    entry_ydl_opts = ydl_opts.copy()
                    entry_ydl_opts['outtmpl'] = entry_file_path

                    await loop.run_in_executor(
                        None,
                        lambda e=entry['url'], opts=entry_ydl_opts: yt_dlp.YoutubeDL(opts).download([
                            e])
                    )

                    # Get the downloaded file name
                    entry_filename = f"{filename}_{idx}.{entry.get('ext', 'mp4')}"
                    files.append(f"/downloads/{entry_filename}")

                return {
                    "session_id": session_id,
                    "status": "completed",
                    "message": f"Downloaded {len(files)} items successfully",
                    # Return first file as main download
                    "download_url": files[0],
                    "additional_files": files[1:] if len(files) > 1 else None
                }
            else:
                # Single post/reel/story
                await loop.run_in_executor(
                    None,
                    lambda: yt_dlp.YoutubeDL(ydl_opts).download([str(url)])
                )

                # Get the real filename with extension
                real_filename = f"{filename}.{info_dict.get('ext', 'mp4')}"

                return {
                    "session_id": session_id,
                    "status": "completed",
                    "message": "Download completed successfully",
                    "download_url": f"/downloads/{real_filename}",
                    "description": info_dict.get('title', ''),
                    "author": info_dict.get('uploader', 'unknown')
                }

        except Exception as e:
            logger.error(f"Instagram download failed for URL {url}: {str(e)}")
            raise DownloadFailedException(str(e))

    async def batch_download(self, urls: List[HttpUrl], quality: str = "best") -> List[dict]:
        """Download multiple Instagram posts"""
        results = []
        for url in urls:
            try:
                result = await self.download_content(url, quality)
                results.append(result)
            except Exception as e:
                logger.error(
                    f"Batch Instagram download failed for URL {url}: {str(e)}")
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
