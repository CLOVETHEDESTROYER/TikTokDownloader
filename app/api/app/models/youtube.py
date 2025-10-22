from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from enum import Enum


class YouTubeContentType(str, Enum):
    VIDEO = "video"
    SHORTS = "shorts"
    PLAYLIST = "playlist"
    LIVE = "live"


class YouTubeQuality(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class YouTubeDownloadRequest(BaseModel):
    url: HttpUrl
    quality: YouTubeQuality = YouTubeQuality.HIGH
    include_metadata: bool = True
    include_subtitles: bool = False

    @validator('url')
    def validate_url(cls, v):
        url_str = str(v).lower()
        if 'youtube.com' not in url_str and 'youtu.be' not in url_str:
            raise ValueError('URL must be from YouTube')
        return v


class YouTubeMediaMetadata(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    duration: Optional[float] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    description: Optional[str] = None
    upload_date: Optional[str] = None
    content_type: YouTubeContentType
    is_shorts: bool = False
    thumbnail_url: Optional[str] = None


class YouTubeDownloadResponse(BaseModel):
    url: str
    download_url: str
    content_type: YouTubeContentType
    metadata: YouTubeMediaMetadata
    session_id: str
    is_shorts: bool = False


class YouTubeBatchDownloadRequest(BaseModel):
    urls: List[HttpUrl]
    quality: YouTubeQuality = YouTubeQuality.HIGH
    include_metadata: bool = True

    @validator('urls')
    def validate_urls(cls, v):
        for url in v:
            url_str = str(url).lower()
            if 'youtube.com' not in url_str and 'youtu.be' not in url_str:
                raise ValueError(f'URL {url} must be from YouTube')
        return v
