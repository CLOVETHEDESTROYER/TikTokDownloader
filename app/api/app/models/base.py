from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Union
from enum import Enum


class Platform(str, Enum):
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"


class DownloadRequest(BaseModel):
    url: HttpUrl
    platform: Optional[Platform] = None
    quality: Optional[str] = "best"


class BatchDownloadRequest(BaseModel):
    urls: List[HttpUrl]
    platform: Optional[Platform] = None
    quality: Optional[str] = "best"


class DownloadResponse(BaseModel):
    session_id: str
    status: str
    message: str
    download_url: Optional[str] = None


class DownloadStatus(BaseModel):
    session_id: str
    status: str
    progress: float
    message: str
    download_url: Optional[str] = None
    error: Optional[str] = None


class QuotaResponse(BaseModel):
    remaining: int
    reset_at: str
    tier: str
