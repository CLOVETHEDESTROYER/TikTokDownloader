import os
import yt_dlp
import uuid
from typing import Dict, Any, List
from ..core.config import settings
from ..core.exceptions import DownloadError

class TikTokService:
    def __init__(self):
        self.download_folder = settings.DOWNLOAD_FOLDER
        os.makedirs(self.download_folder, exist_ok=True)

    def _get_ydl_opts(self, filename: str) -> dict:
        """Get yt-dlp options optimized for TikTok downloads without watermark."""
        return {
            'outtmpl': os.path.join(self.download_folder, filename),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet': False,
            'noplaylist': True,
            'format_sort': ['res:1080', 'ext:mp4:m4a']
        }

    async def download_video(self, url: str) -> Dict[str, Any]:
        """Download a TikTok video without watermark."""
        filename = f"tiktok_{uuid.uuid4().hex[:8]}.mp4"
        
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
            raise DownloadError(f"Failed to download TikTok video: {str(e)}")

    async def batch_download(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Download multiple TikTok videos."""
        results = []
        for url in urls:
            try:
                result = await self.download_video(url)
                results.append(result)
            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e),
                    'success': False
                })
        return results
