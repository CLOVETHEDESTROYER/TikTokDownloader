from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
import uuid


class SocialPlatform(str, Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"


class ContentType(str, Enum):
    VIDEO = "video"
    POST = "post"
    REEL = "reel"
    STORY = "story"
    IGTV = "igtv"


class ContentStatus(str, Enum):
    COLLECTED = "collected"
    DOWNLOADING = "downloading"
    DOWNLOADED = "downloaded"
    PROCESSING = "processing"
    SCHEDULED = "scheduled"
    POSTED = "posted"
    FAILED = "failed"
    DELETED = "deleted"


class PostStatus(str, Enum):
    SCHEDULED = "scheduled"
    POSTING = "posting"
    POSTED = "posted"
    FAILED = "failed"


class SocialAccount(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    platform: SocialPlatform
    account_id: str
    username: str
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class ContentItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_account_id: str
    original_url: HttpUrl
    platform: SocialPlatform
    content_type: ContentType
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[float] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    status: ContentStatus = ContentStatus.COLLECTED
    download_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class DownloadQueue(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_item_id: str
    priority: int = 0
    status: str = "pending"
    retry_count: int = 0
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ScheduledPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_item_id: str
    target_platforms: List[SocialPlatform]
    scheduled_time: datetime
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None
    status: PostStatus = PostStatus.SCHEDULED
    post_data: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    posted_at: Optional[datetime] = None


class InstagramOAuthRequest(BaseModel):
    code: str
    redirect_uri: str


class InstagramOAuthResponse(BaseModel):
    access_token: str
    user_id: str
    username: str
    expires_in: Optional[int] = None


class ContentCollectionRequest(BaseModel):
    account_id: str
    content_types: Optional[List[ContentType]] = [
        ContentType.POST, ContentType.REEL]
    limit: Optional[int] = 50


class ContentCollectionResponse(BaseModel):
    collected_count: int
    new_content: List[ContentItem]
    existing_content: List[ContentItem]
    errors: Optional[List[str]] = None


class DashboardStats(BaseModel):
    total_accounts: int
    active_accounts: int
    total_content_collected: int
    content_by_status: Dict[str, int]
    downloads_pending: int
    scheduled_posts: int
    recent_activity: List[Dict[str, Any]]
