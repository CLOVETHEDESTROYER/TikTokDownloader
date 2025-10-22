from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from enum import Enum


class Platform(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"


class VideoQuality(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DownloadRequest(BaseModel):
    url: HttpUrl
    platform: Platform
    quality: VideoQuality = VideoQuality.HIGH

    @validator('url')
    def validate_url(cls, v, values):
        url_str = str(v).lower()
        platform = values.get('platform')

        if platform == Platform.TIKTOK and 'tiktok.com' not in url_str:
            raise ValueError('URL must be from TikTok')
        elif platform == Platform.INSTAGRAM and 'instagram.com' not in url_str:
            raise ValueError('URL must be from Instagram')
        elif platform == Platform.YOUTUBE and 'youtube.com' not in url_str and 'youtu.be' not in url_str:
            raise ValueError('URL must be from YouTube')
        elif platform == Platform.FACEBOOK and 'facebook.com' not in url_str and 'fb.watch' not in url_str:
            raise ValueError('URL must be from Facebook')
        return v


class DownloadStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class DownloadResponse(BaseModel):
    session_id: str
    status: DownloadStatus
    progress: int = 0
    url: HttpUrl
    filename: Optional[str] = None
    error: Optional[str] = None
    expires_at: Optional[float] = None
    # Video metadata
    title: Optional[str] = None
    author: Optional[str] = None
    duration: Optional[float] = None
    thumbnail: Optional[str] = None


class BatchDownloadRequest(BaseModel):
    urls: List[HttpUrl]
    platform: Platform
    quality: VideoQuality = VideoQuality.HIGH

    @validator('urls')
    def validate_urls(cls, v, values):
        platform = values.get('platform')
        for url in v:
            url_str = str(url).lower()
            if platform == Platform.TIKTOK and 'tiktok.com' not in url_str:
                raise ValueError(f'URL {url} must be from TikTok')
            elif platform == Platform.INSTAGRAM and 'instagram.com' not in url_str:
                raise ValueError(f'URL {url} must be from Instagram')
            elif platform == Platform.YOUTUBE and 'youtube.com' not in url_str and 'youtu.be' not in url_str:
                raise ValueError(f'URL {url} must be from YouTube')
            elif platform == Platform.FACEBOOK and 'facebook.com' not in url_str and 'fb.watch' not in url_str:
                raise ValueError(f'URL {url} must be from Facebook')
        return v


class DownloadStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class BatchDownloadResponse(BaseModel):
    session_id: str
    total_urls: int
    processed_urls: int = 0
    status: DownloadStatus
    progress: int = 0
    expires_at: Optional[float] = None
