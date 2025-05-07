from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from enum import Enum


class InstagramMediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    STORY = "story"
    REEL = "reel"


class InstagramQuality(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class InstagramDownloadRequest(BaseModel):
    url: HttpUrl
    quality: InstagramQuality = InstagramQuality.HIGH
    include_caption: bool = False
    include_metadata: bool = False


class InstagramMediaMetadata(BaseModel):
    caption: Optional[str] = None
    author: Optional[str] = None
    timestamp: Optional[str] = None
    likes: Optional[int] = None
    media_type: InstagramMediaType
    duration: Optional[float] = None  # for videos only


class InstagramDownloadResponse(BaseModel):
    url: str
    download_url: str
    media_type: InstagramMediaType
    metadata: InstagramMediaMetadata
    session_id: str
