from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from enum import Enum


class FacebookContentType(str, Enum):
    VIDEO = "video"
    REEL = "reel"
    LIVE = "live"
    STORY = "story"
    POST = "post"


class FacebookQuality(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FacebookDownloadRequest(BaseModel):
    url: HttpUrl
    quality: FacebookQuality = FacebookQuality.HIGH
    include_metadata: bool = True
    include_captions: bool = False

    @validator('url')
    def validate_url(cls, v):
        url_str = str(v).lower()
        if 'facebook.com' not in url_str and 'fb.watch' not in url_str:
            raise ValueError('URL must be from Facebook')
        return v


class FacebookMediaMetadata(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    duration: Optional[float] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    description: Optional[str] = None
    upload_date: Optional[str] = None
    content_type: FacebookContentType
    is_live: bool = False
    thumbnail_url: Optional[str] = None
    page_name: Optional[str] = None


class FacebookDownloadResponse(BaseModel):
    url: str
    download_url: str
    content_type: FacebookContentType
    metadata: FacebookMediaMetadata
    session_id: str
    is_live: bool = False


class FacebookBatchDownloadRequest(BaseModel):
    urls: List[HttpUrl]
    quality: FacebookQuality = FacebookQuality.HIGH
    include_metadata: bool = True

    @validator('urls')
    def validate_urls(cls, v):
        for url in v:
            url_str = str(url).lower()
            if 'facebook.com' not in url_str and 'fb.watch' not in url_str:
                raise ValueError(f'URL {url} must be from Facebook')
        return v
