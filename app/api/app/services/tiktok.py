import yt_dlp
import os
import uuid
from typing import List
from pydantic import HttpUrl
from ..core.config import settings
from ..core.exceptions import DownloadFailedException, InvalidURLException

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
    
    async def download_video(self, url: HttpUrl, quality: str = "best") -> dict:
        """Download a single TikTok video"""
        session_id = str(uuid.uuid4())
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extract video info first
                info = ydl.extract_info(str(url), download=False)
                if not info:
                    raise InvalidURLException("TikTok")
                
                # Download the video
                ydl.download([str(url)])
                
                # Construct download URL
                filename = f"{info['id']}.{info['ext']}"
                file_path = os.path.join(self.download_path, filename)
                
                return {
                    "session_id": session_id,
                    "status": "completed",
                    "message": "Download completed successfully",
                    "download_url": f"/downloads/{filename}"
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