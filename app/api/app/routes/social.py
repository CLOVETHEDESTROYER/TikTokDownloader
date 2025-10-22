from fastapi import APIRouter, Depends, Header, HTTPException, Query
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from app.models.social import (
    SocialAccount,
    ContentItem,
    ContentCollectionRequest,
    ContentCollectionResponse,
    DashboardStats,
    InstagramOAuthRequest,
    InstagramOAuthResponse,
    SocialPlatform,
    ContentType
)
from app.core.exceptions import UnauthorizedException
from app.core.config import settings
from app.services.social.instagram_connector import InstagramConnector

router = APIRouter(prefix="/api/v1/social", tags=["social"])


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


@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(api_key: str = Depends(verify_api_key)):
    """Get dashboard statistics"""
    # This would query your database for real stats
    # For now, return mock data
    return DashboardStats(
        total_accounts=3,
        active_accounts=2,
        total_content_collected=45,
        content_by_status={
            "collected": 15,
            "downloading": 5,
            "downloaded": 20,
            "scheduled": 3,
            "posted": 2
        },
        downloads_pending=8,
        scheduled_posts=3,
        recent_activity=[
            {
                "type": "content_collected",
                "platform": "instagram",
                "count": 5,
                "timestamp": "2025-09-15T16:30:00Z"
            },
            {
                "type": "post_scheduled",
                "platform": "tiktok",
                "count": 2,
                "timestamp": "2025-09-15T16:25:00Z"
            }
        ]
    )


@router.get("/accounts", response_model=List[SocialAccount])
async def get_social_accounts(api_key: str = Depends(verify_api_key)):
    """Get all connected social media accounts"""
    # This would query your database
    # For now, return mock data
    return [
        SocialAccount(
            platform=SocialPlatform.INSTAGRAM,
            account_id="instagram_user_123",
            username="your_instagram_username",
            access_token="mock_token",
            is_active=True
        )
    ]


@router.post("/instagram/connect", response_model=InstagramOAuthResponse)
async def connect_instagram_account(
    request: InstagramOAuthRequest,
    api_key: str = Depends(verify_api_key)
):
    """Connect Instagram account via OAuth"""
    connector = InstagramConnector()

    try:
        oauth_response = await connector.exchange_code_for_token(request.code)

        # Save account to database (implement this)
        # account = SocialAccount(
        #     platform=SocialPlatform.INSTAGRAM,
        #     account_id=oauth_response.user_id,
        #     username=oauth_response.username,
        #     access_token=oauth_response.access_token
        # )
        # await save_account_to_db(account)

        return oauth_response

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to connect Instagram: {str(e)}")


@router.get("/instagram/auth-url")
async def get_instagram_auth_url(
    state: Optional[str] = Query(None),
    api_key: str = Depends(verify_api_key)
):
    """Get Instagram OAuth authorization URL"""
    connector = InstagramConnector()
    auth_url = connector.get_auth_url(state)

    return {"auth_url": auth_url}


@router.post("/instagram/collect-saved", response_model=ContentCollectionResponse)
async def collect_instagram_saved_posts(
    account_id: str = Query(..., description="Instagram account ID"),
    limit: int = Query(50, description="Maximum number of posts to collect"),
    api_key: str = Depends(verify_api_key)
):
    """Collect saved posts from Instagram account"""
    connector = InstagramConnector()

    # Get account from database (implement this)
    # account = await get_account_by_id(account_id)
    # if not account:
    #     raise HTTPException(status_code=404, detail="Account not found")

    # For now, create a mock account
    account = SocialAccount(
        platform=SocialPlatform.INSTAGRAM,
        account_id=account_id,
        username="mock_user",
        access_token="mock_token"
    )

    try:
        result = await connector.collect_saved_content(account, limit)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to collect saved posts: {str(e)}")


@router.post("/instagram/collect-liked", response_model=ContentCollectionResponse)
async def collect_instagram_liked_posts(
    account_id: str = Query(..., description="Instagram account ID"),
    limit: int = Query(50, description="Maximum number of posts to collect"),
    api_key: str = Depends(verify_api_key)
):
    """Collect liked posts from Instagram account"""
    connector = InstagramConnector()

    # Get account from database (implement this)
    account = SocialAccount(
        platform=SocialPlatform.INSTAGRAM,
        account_id=account_id,
        username="mock_user",
        access_token="mock_token"
    )

    try:
        result = await connector.collect_liked_content(account, limit)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to collect liked posts: {str(e)}")


@router.get("/content", response_model=List[ContentItem])
async def get_collected_content(
    platform: Optional[SocialPlatform] = Query(None),
    content_type: Optional[ContentType] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50),
    api_key: str = Depends(verify_api_key)
):
    """Get collected content with optional filters"""
    # This would query your database with filters
    # For now, return mock data
    mock_content = [
        ContentItem(
            source_account_id="account_1",
            original_url="https://www.instagram.com/p/C1234567890/",
            platform=SocialPlatform.INSTAGRAM,
            content_type=ContentType.REEL,
            title="Amazing dance reel",
            description="Check out this awesome dance move!",
            status="collected"
        ),
        ContentItem(
            source_account_id="account_1",
            original_url="https://www.instagram.com/p/mock_post_2/",
            platform=SocialPlatform.INSTAGRAM,
            content_type=ContentType.POST,
            title="Beautiful sunset",
            description="Sunset from my vacation",
            status="downloaded"
        )
    ]

    # Apply filters (mock implementation)
    filtered_content = mock_content
    if platform:
        filtered_content = [
            c for c in filtered_content if c.platform == platform]
    if content_type:
        filtered_content = [
            c for c in filtered_content if c.content_type == content_type]
    if status:
        filtered_content = [c for c in filtered_content if c.status == status]

    return filtered_content[:limit]


@router.post("/content/{content_id}/download")
async def add_to_download_queue(
    content_id: str,
    priority: int = Query(
        0, description="Download priority (0=normal, 1=high)"),
    api_key: str = Depends(verify_api_key)
):
    """Add content item to download queue"""
    from app.services.social.download_queue import download_queue_service

    try:
        # Get content item (mock implementation)
        content_item = ContentItem(
            id=content_id,
            source_account_id="mock_account",
            original_url="https://example.com/mock",
            platform="instagram",
            content_type="reel",
            status="collected"
        )

        queue_id = await download_queue_service.add_to_queue(content_item, priority)

        return {
            "message": f"Content {content_id} added to download queue",
            "content_id": content_id,
            "queue_id": queue_id,
            "priority": priority,
            "status": "queued"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add to download queue: {str(e)}")


@router.delete("/content/{content_id}")
async def delete_content_item(
    content_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Delete content item and associated files"""
    # This would delete the content item and any downloaded files
    return {
        "message": f"Content {content_id} deleted successfully",
        "content_id": content_id
    }


@router.get("/accounts/{account_id}/status")
async def get_account_status(
    account_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get account connection status and health"""
    # This would check the account's token validity and connection status
    return {
        "account_id": account_id,
        "status": "connected",
        "last_sync": "2025-09-15T16:30:00Z",
        "token_expires": "2025-10-15T16:30:00Z",
        "is_valid": True
    }


@router.get("/download-queue/status")
async def get_download_queue_status(api_key: str = Depends(verify_api_key)):
    """Get download queue status"""
    from app.services.social.download_queue import download_queue_service

    try:
        status = await download_queue_service.get_queue_status()
        return status
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get queue status: {str(e)}")


@router.post("/download-queue/clear-failed")
async def clear_failed_downloads(api_key: str = Depends(verify_api_key)):
    """Clear all failed downloads from queue"""
    from app.services.social.download_queue import download_queue_service

    try:
        await download_queue_service.clear_failed_items()
        return {"message": "Failed downloads cleared from queue"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to clear failed downloads: {str(e)}")
