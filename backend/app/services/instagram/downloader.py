import os
import yt_dlp
import uuid
from typing import Optional, Dict, Any
from ...core.config import settings
from ...models.instagram import InstagramDownloadRequest, InstagramDownloadResponse, InstagramMediaType
from ...core.exceptions import DownloadError, InvalidURLError
from .utils import load_cookies, validate_instagram_url, get_media_type, clean_filename


class InstagramDownloader:
    def __init__(self):
        self.cookies = load_cookies()
        self.download_folder = settings.DOWNLOAD_FOLDER
        os.makedirs(self.download_folder, exist_ok=True)

    async def download(self, request: InstagramDownloadRequest) -> InstagramDownloadResponse:
        """Download Instagram content."""
        if not validate_instagram_url(str(request.url)):
            raise InvalidURLError("Invalid Instagram URL")

        session_id = str(uuid.uuid4())
        output_path = os.path.join(
            self.download_folder, f"{session_id}/%(title)s.%(ext)s")

        ydl_opts = {
            'format': self._get_format_for_quality(request.quality),
            'outtmpl': output_path,
            'cookiefile': settings.INSTAGRAM_COOKIES_FILE,
            'extract_flat': True,
            'quiet': True,
            'no_warnings': True,
            'retries': settings.INSTAGRAM_MAX_RETRIES,
            'socket_timeout': settings.INSTAGRAM_TIMEOUT
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(str(request.url), download=False)
                media_type = self._determine_media_type(info)

                # Download the content
                ydl.download([str(request.url)])

                # Get downloaded file info
                filename = ydl.prepare_filename(info)
                download_url = f"/downloads/{session_id}/{os.path.basename(filename)}"

                return InstagramDownloadResponse(
                    url=str(request.url),
                    download_url=download_url,
                    media_type=media_type,
                    metadata=self._extract_metadata(info),
                    session_id=session_id
                )

        except Exception as e:
            raise DownloadError(
                f"Failed to download Instagram content: {str(e)}")

    def _get_format_for_quality(self, quality: str) -> str:
        """Get yt-dlp format string based on quality."""
        quality_map = {
            'high': 'bestvideo+bestaudio/best',
            'medium': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            'low': 'bestvideo[height<=480]+bestaudio/best[height<=480]'
        }
        return quality_map.get(quality.lower(), 'best')

    def _determine_media_type(self, info: Dict[str, Any]) -> InstagramMediaType:
        """Determine the type of Instagram media from the extracted info."""
        if info.get('_type') == 'playlist':
            return InstagramMediaType.CAROUSEL
        elif info.get('is_story'):
            return InstagramMediaType.STORY
        elif info.get('is_reel'):
            return InstagramMediaType.REEL
        elif info.get('duration'):
            return InstagramMediaType.VIDEO
        return InstagramMediaType.IMAGE

    def _extract_metadata(self, info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant metadata from the downloaded content."""
        return {
            'caption': info.get('description'),
            'author': info.get('uploader'),
            'timestamp': info.get('timestamp'),
            'likes': info.get('like_count'),
            'media_type': self._determine_media_type(info),
            'duration': info.get('duration')
        }


if __name__ == "__main__":
    url = input("Paste the Instagram post/reel/video URL: ").strip()
    download_instagram_video(url)
