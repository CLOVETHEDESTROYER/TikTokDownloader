from fastapi import APIRouter, Depends, HTTPException, Header, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.social import (
    SocialPlatform,
    ContentStatus,
    ScheduledPost,
    SocialAccount
)
from app.core.exceptions import UnauthorizedException
from app.core.config import settings
from app.services.social.publishing_manager import publishing_manager

router = APIRouter(prefix="/api/v1/publishing", tags=["publishing"])

def verify_api_key(x_api_key: str = Header(None)):
    # Skip API key check in development mode if configured
    if settings.ENV == "development" and not settings.REQUIRE_API_KEY:
        return x_api_key

    if not x_api_key:
        raise UnauthorizedException("API key is missing")

    # Check if the API key matches either the admin key or the website key
    if (settings.ADMIN_API_KEY and x_api_key == settings.ADMIN_API_KEY) or \
       (settings.WEBSITE_API_KEY and x_api_key == settings.WEBSITE_API_KEY):
        return x_api_key

    raise UnauthorizedException("Invalid API key")

# Mock database for scheduled posts and accounts
mock_scheduled_posts: Dict[str, ScheduledPost] = {}
mock_social_accounts: Dict[str, SocialAccount] = {}

@router.post("/schedule")
async def schedule_post(
    content_id: str = Query(...),
    target_platforms: List[SocialPlatform] = Query(...),
    scheduled_time: datetime = Query(...),
    caption: str = Query(""),
    hashtags: List[str] = Query(default=[]),
    privacy_level: str = Query("PUBLIC_TO_EVERYONE", description="TikTok privacy level"),
    location_id: Optional[str] = Query(None, description="Instagram location ID"),
    api_key: str = Depends(verify_api_key)
):
    """Schedule a post for publishing at a specific time."""
    try:
        # Mock content item (in real app, fetch from database)
        from app.models.social import ContentItem, ContentType
        content_item = ContentItem(
            id=content_id,
            source_account_id="mock_account",
            original_url="https://example.com/mock",
            platform=SocialPlatform.INSTAGRAM,
            content_type=ContentType.VIDEO,
            status=ContentStatus.DOWNLOADED,
            download_path="/mock/path/video.mp4"
        )
        
        scheduled_post_id = await publishing_manager.schedule_post(
            content_item=content_item,
            target_platforms=target_platforms,
            scheduled_time=scheduled_time,
            caption=caption,
            hashtags=hashtags,
            privacy_level=privacy_level,
            location_id=location_id
        )
        
        return {
            "success": True,
            "scheduled_post_id": scheduled_post_id,
            "content_id": content_id,
            "target_platforms": target_platforms,
            "scheduled_time": scheduled_time.isoformat(),
            "message": "Post scheduled successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule post: {str(e)}")

@router.post("/publish-now")
async def publish_now(
    content_id: str = Query(...),
    target_platforms: List[SocialPlatform] = Query(...),
    caption: str = Query(""),
    hashtags: List[str] = Query(default=[]),
    privacy_level: str = Query("PUBLIC_TO_EVERYONE", description="TikTok privacy level"),
    location_id: Optional[str] = Query(None, description="Instagram location ID"),
    api_key: str = Depends(verify_api_key)
):
    """Publish content immediately to specified platforms."""
    try:
        # Mock content item and accounts (in real app, fetch from database)
        from app.models.social import ContentItem, ContentType
        content_item = ContentItem(
            id=content_id,
            source_account_id="mock_account",
            original_url="https://example.com/mock",
            platform=SocialPlatform.INSTAGRAM,
            content_type=ContentType.VIDEO,
            status=ContentStatus.DOWNLOADED,
            download_path="/mock/path/video.mp4"
        )
        
        # Mock accounts for each platform
        accounts = {}
        for platform in target_platforms:
            if platform == SocialPlatform.TIKTOK:
                accounts[platform] = SocialAccount(
                    id=f"tiktok_{platform}",
                    user_id="mock_user",
                    platform=platform,
                    account_id="mock_tiktok_id",
                    username="mock_tiktok_user",
                    access_token="mock_tiktok_token",
                    expires_at=datetime.now() + timedelta(days=30)
                )
            elif platform == SocialPlatform.INSTAGRAM:
                accounts[platform] = SocialAccount(
                    id=f"instagram_{platform}",
                    user_id="mock_user",
                    platform=platform,
                    account_id="mock_instagram_id",
                    username="mock_instagram_user",
                    access_token="mock_instagram_token",
                    expires_at=datetime.now() + timedelta(days=30)
                )
        
        result = await publishing_manager.publish_now(
            content_item=content_item,
            target_platforms=target_platforms,
            accounts=accounts,
            caption=caption,
            hashtags=hashtags,
            privacy_level=privacy_level,
            location_id=location_id
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish content: {str(e)}")

@router.get("/scheduled-posts")
async def list_scheduled_posts(
    platform: Optional[SocialPlatform] = Query(None),
    status: Optional[ContentStatus] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    api_key: str = Depends(verify_api_key)
):
    """List all scheduled posts with optional filters."""
    # In a real implementation, this would query the database
    scheduled_posts = list(mock_scheduled_posts.values())
    
    if platform:
        scheduled_posts = [p for p in scheduled_posts if platform in p.target_platforms]
    
    return {
        "scheduled_posts": scheduled_posts[:limit],
        "total_count": len(scheduled_posts),
        "filters": {
            "platform": platform,
            "status": status,
            "limit": limit
        }
    }

@router.get("/scheduled-posts/{scheduled_post_id}")
async def get_scheduled_post(
    scheduled_post_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get details of a specific scheduled post."""
    scheduled_post = mock_scheduled_posts.get(scheduled_post_id)
    if not scheduled_post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")
    
    return scheduled_post

@router.delete("/scheduled-posts/{scheduled_post_id}")
async def cancel_scheduled_post(
    scheduled_post_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Cancel a scheduled post."""
    try:
        success = await publishing_manager.cancel_scheduled_post(scheduled_post_id)
        if success:
            if scheduled_post_id in mock_scheduled_posts:
                del mock_scheduled_posts[scheduled_post_id]
            return {
                "success": True,
                "message": f"Scheduled post {scheduled_post_id} cancelled successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to cancel scheduled post")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel scheduled post: {str(e)}")

@router.get("/status/{content_id}")
async def get_publish_status(
    content_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get publishing status for a content item."""
    try:
        status = await publishing_manager.get_publish_status(content_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get publish status: {str(e)}")

@router.post("/delete-published")
async def delete_published_content(
    content_id: str,
    platform: SocialPlatform,
    account_id: str,
    media_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Delete published content from a platform."""
    try:
        # Get account (in real app, fetch from database)
        account = mock_social_accounts.get(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        result = await publishing_manager.delete_published_content(
            content_id=content_id,
            platform=platform,
            account=account,
            media_id=media_id
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete published content: {str(e)}")

@router.post("/cleanup/{content_id}")
async def cleanup_after_publish(
    content_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Clean up local files after successful publishing."""
    try:
        # Mock content item (in real app, fetch from database)
        from app.models.social import ContentItem, ContentType
        content_item = ContentItem(
            id=content_id,
            source_account_id="mock_account",
            original_url="https://example.com/mock",
            platform=SocialPlatform.INSTAGRAM,
            content_type=ContentType.VIDEO,
            status=ContentStatus.POSTED,
            download_path="/mock/path/video.mp4"
        )
        
        success = await publishing_manager.cleanup_after_publish(content_item)
        
        return {
            "success": success,
            "content_id": content_id,
            "message": "Cleanup completed" if success else "Cleanup failed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cleanup content: {str(e)}")

@router.get("/platforms")
async def get_supported_platforms(api_key: str = Depends(verify_api_key)):
    """Get list of supported publishing platforms."""
    return {
        "supported_platforms": [
            {
                "platform": "tiktok",
                "name": "TikTok",
                "features": ["video", "caption", "hashtags", "privacy_settings"],
                "max_video_duration": 180,  # seconds
                "max_file_size": 500  # MB
            },
            {
                "platform": "instagram",
                "name": "Instagram",
                "features": ["video", "caption", "hashtags", "location"],
                "max_video_duration": 60,  # seconds for reels
                "max_file_size": 100  # MB
            }
        ]
    }
