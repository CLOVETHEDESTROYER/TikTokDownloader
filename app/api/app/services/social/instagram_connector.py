import httpx
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.social import (
    SocialAccount, 
    ContentItem, 
    ContentType, 
    ContentStatus,
    InstagramOAuthResponse,
    ContentCollectionResponse
)

logger = logging.getLogger(__name__)


class InstagramConnector:
    def __init__(self):
        self.base_url = "https://graph.instagram.com"
        self.api_version = "v18.0"
        self.client_id = settings.INSTAGRAM_APP_ID
        self.client_secret = settings.INSTAGRAM_APP_SECRET
        self.redirect_uri = settings.INSTAGRAM_REDIRECT_URI

    async def exchange_code_for_token(self, code: str) -> InstagramOAuthResponse:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
                "code": code
            }
            
            response = await client.post(
                f"{self.base_url}/oauth/access_token",
                data=data
            )
            response.raise_for_status()
            
            token_data = response.json()
            
            # Get user info
            user_info = await self.get_user_info(token_data["access_token"])
            
            return InstagramOAuthResponse(
                access_token=token_data["access_token"],
                user_id=user_info["id"],
                username=user_info["username"],
                expires_in=token_data.get("expires_in")
            )

    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get Instagram user information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{self.api_version}/me",
                params={
                    "fields": "id,username,account_type,media_count",
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_user_media(self, access_token: str, user_id: str, 
                           limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's media (posts, reels, etc.)"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{self.api_version}/{user_id}/media",
                params={
                    "fields": "id,media_type,media_url,thumbnail_url,caption,timestamp,permalink,like_count,comments_count",
                    "limit": limit,
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            return response.json().get("data", [])

    async def get_saved_posts(self, access_token: str, user_id: str,
                            limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's saved posts"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{self.api_version}/{user_id}/saved",
                params={
                    "fields": "id,media_type,media_url,thumbnail_url,caption,timestamp,permalink,like_count,comments_count",
                    "limit": limit,
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            return response.json().get("data", [])

    async def get_liked_posts(self, access_token: str, user_id: str,
                            limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's liked posts"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{self.api_version}/{user_id}/likes",
                params={
                    "fields": "id,media_type,media_url,thumbnail_url,caption,timestamp,permalink,like_count,comments_count",
                    "limit": limit,
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            return response.json().get("data", [])

    def determine_content_type(self, media_data: Dict[str, Any]) -> ContentType:
        """Determine content type from Instagram media data"""
        media_type = media_data.get("media_type", "").lower()
        
        if media_type == "video":
            # Check if it's a reel (typically shorter videos)
            caption = media_data.get("caption", "").lower()
            if "reel" in caption or "#reel" in caption:
                return ContentType.REEL
            return ContentType.POST
        elif media_type == "carousel_album":
            return ContentType.POST
        elif media_type == "story":
            return ContentType.STORY
        else:
            return ContentType.POST

    async def collect_saved_content(self, account: SocialAccount, 
                                  limit: int = 50) -> ContentCollectionResponse:
        """Collect saved posts from Instagram account"""
        try:
            # Get saved posts
            saved_posts = await self.get_saved_posts(
                account.access_token, 
                account.account_id, 
                limit
            )
            
            new_content = []
            existing_content = []
            errors = []
            
            for post_data in saved_posts:
                try:
                    # Check if content already exists
                    existing_item = await self._check_existing_content(
                        post_data.get("permalink", "")
                    )
                    
                    if existing_item:
                        existing_content.append(existing_item)
                        continue
                    
                    # Create new content item
                    content_item = await self._create_content_item(
                        post_data, account, ContentStatus.COLLECTED
                    )
                    new_content.append(content_item)
                    
                except Exception as e:
                    logger.error(f"Error processing post {post_data.get('id')}: {e}")
                    errors.append(f"Post {post_data.get('id')}: {str(e)}")
            
            return ContentCollectionResponse(
                collected_count=len(new_content),
                new_content=new_content,
                existing_content=existing_content,
                errors=errors if errors else None
            )
            
        except Exception as e:
            logger.error(f"Error collecting saved content: {e}")
            return ContentCollectionResponse(
                collected_count=0,
                new_content=[],
                existing_content=[],
                errors=[str(e)]
            )

    async def collect_liked_content(self, account: SocialAccount,
                                  limit: int = 50) -> ContentCollectionResponse:
        """Collect liked posts from Instagram account"""
        try:
            # Get liked posts
            liked_posts = await self.get_liked_posts(
                account.access_token,
                account.account_id,
                limit
            )
            
            new_content = []
            existing_content = []
            errors = []
            
            for post_data in liked_posts:
                try:
                    # Check if content already exists
                    existing_item = await self._check_existing_content(
                        post_data.get("permalink", "")
                    )
                    
                    if existing_item:
                        existing_content.append(existing_item)
                        continue
                    
                    # Create new content item
                    content_item = await self._create_content_item(
                        post_data, account, ContentStatus.COLLECTED
                    )
                    new_content.append(content_item)
                    
                except Exception as e:
                    logger.error(f"Error processing liked post {post_data.get('id')}: {e}")
                    errors.append(f"Post {post_data.get('id')}: {str(e)}")
            
            return ContentCollectionResponse(
                collected_count=len(new_content),
                new_content=new_content,
                existing_content=existing_content,
                errors=errors if errors else None
            )
            
        except Exception as e:
            logger.error(f"Error collecting liked content: {e}")
            return ContentCollectionResponse(
                collected_count=0,
                new_content=[],
                existing_content=[],
                errors=[str(e)]
            )

    async def _check_existing_content(self, url: str) -> Optional[ContentItem]:
        """Check if content already exists in database"""
        # This would query your database
        # For now, return None (not implemented)
        return None

    async def _create_content_item(self, post_data: Dict[str, Any], 
                                 account: SocialAccount, 
                                 status: ContentStatus) -> ContentItem:
        """Create ContentItem from Instagram post data"""
        content_type = self.determine_content_type(post_data)
        
        # Extract metadata
        metadata = {
            "instagram_id": post_data.get("id"),
            "media_type": post_data.get("media_type"),
            "timestamp": post_data.get("timestamp"),
            "like_count": post_data.get("like_count", 0),
            "comments_count": post_data.get("comments_count", 0)
        }
        
        return ContentItem(
            source_account_id=account.id,
            original_url=post_data.get("permalink", ""),
            platform=account.platform,
            content_type=content_type,
            title=post_data.get("caption", "")[:100] if post_data.get("caption") else None,
            description=post_data.get("caption"),
            thumbnail_url=post_data.get("thumbnail_url") or post_data.get("media_url"),
            metadata=metadata,
            status=status
        )

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh Instagram access token"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/refresh_access_token",
                params={
                    "grant_type": "ig_refresh_token",
                    "access_token": refresh_token
                }
            )
            response.raise_for_status()
            return response.json()

    def get_auth_url(self, state: str = None) -> str:
        """Generate Instagram OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "user_profile,user_media",
            "response_type": "code"
        }
        
        if state:
            params["state"] = state
            
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://api.instagram.com/oauth/authorize?{query_string}"
