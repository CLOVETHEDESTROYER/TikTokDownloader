from enum import Enum, auto
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Platform(str, Enum):
    """Video platform enumeration"""
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TWITTER = "twitter"

class VideoQuality(str, Enum):
    """Video quality enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class VideoMetadata(BaseModel):
    """Video metadata model"""
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    platform: Platform
    quality: VideoQuality = VideoQuality.MEDIUM
    url: str
    
class VideoDownloadRequest(BaseModel):
    """Request model for video download"""
    url: str
    quality: VideoQuality = VideoQuality.MEDIUM
    
class VideoResponse(BaseModel):
    """Response model for video information"""
    id: str
    thumbnail: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    duration: Optional[int] = None
    download_url: str
    session_id: str
    quality: str
    filename: Optional[str] = None 