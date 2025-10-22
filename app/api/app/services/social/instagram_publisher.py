import httpx
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.core.config import settings
from app.models.social import SocialAccount, ContentItem, ScheduledPost, ContentStatus

logger = logging.getLogger(__name__)


class InstagramPublisher:
    def __init__(self):
        self.graph_api_base_url = "https://graph.instagram.com"
        
    async def publish_video(
        self, 
        account: SocialAccount, 
        content_item: ContentItem, 
        video_path: str,
        caption: str = "",
        hashtags: list = None,
        location_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Publish a video to Instagram using the Instagram Graph API.
        
        Args:
            account: Instagram social account with access token
            content_item: Content item being published
            video_path: Local path to the video file
            caption: Video caption/description
            hashtags: List of hashtags to include
            location_id: Optional location ID for the post
            
        Returns:
            Dict containing publish result and media ID
        """
        try:
            logger.info(f"Starting Instagram video publish for content {content_item.id}")
            
            # Prepare hashtags
            if hashtags:
                hashtag_string = " ".join([f"#{tag}" for tag in hashtags])
                full_caption = f"{caption}\n\n{hashtag_string}".strip()
            else:
                full_caption = caption
                
            # Step 1: Create media container
            container_response = await self._create_media_container(
                account.access_token,
                video_path,
                full_caption,
                location_id
            )
            
            if not container_response.get('id'):
                raise Exception(f"Failed to create media container: {container_response}")
                
            container_id = container_response['id']
            
            # Step 2: Publish the media
            publish_result = await self._publish_media(account.access_token, container_id)
            
            if publish_result.get('id'):
                logger.info(f"Successfully published Instagram video for content {content_item.id}")
                return {
                    "success": True,
                    "platform": "instagram",
                    "media_id": publish_result['id'],
                    "container_id": container_id,
                    "published_at": datetime.now().isoformat(),
                    "caption": full_caption
                }
            else:
                raise Exception(f"Failed to publish media: {publish_result}")
                
        except Exception as e:
            logger.error(f"Instagram publish failed for content {content_item.id}: {str(e)}")
            return {
                "success": False,
                "platform": "instagram",
                "error": str(e),
                "content_id": content_item.id
            }
    
    async def _create_media_container(
        self, 
        access_token: str, 
        video_path: str, 
        caption: str,
        location_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a media container for video upload."""
        # First, upload the video file to get a media ID
        media_id = await self._upload_video_file(access_token, video_path)
        
        # Then create the container
        async with httpx.AsyncClient() as client:
            data = {
                "media_type": "VIDEO",
                "video_id": media_id,
                "caption": caption,
                "access_token": access_token
            }
            
            if location_id:
                data["location_id"] = location_id
                
            response = await client.post(
                f"{self.graph_api_base_url}/{account.account_id}/media",
                data=data
            )
            response.raise_for_status()
            return response.json()
    
    async def _upload_video_file(self, access_token: str, video_path: str) -> str:
        """Upload video file and return media ID."""
        async with httpx.AsyncClient() as client:
            with open(video_path, 'rb') as video_file:
                response = await client.post(
                    f"{self.graph_api_base_url}/v18.0/me/media",
                    files={"video": video_file},
                    data={
                        "access_token": access_token,
                        "media_type": "VIDEO"
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result['id']
    
    async def _publish_media(self, access_token: str, container_id: str) -> Dict[str, Any]:
        """Publish the media container."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.graph_api_base_url}/{account.account_id}/media_publish",
                data={
                    "creation_id": container_id,
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def get_media_status(self, access_token: str, media_id: str) -> Dict[str, Any]:
        """Get the status of a published media."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.graph_api_base_url}/{media_id}",
                params={
                    "fields": "id,media_type,media_url,permalink,thumbnail_url,timestamp,caption",
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def delete_media(self, access_token: str, media_id: str) -> Dict[str, Any]:
        """Delete a published media."""
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.graph_api_base_url}/{media_id}",
                params={"access_token": access_token}
            )
            response.raise_for_status()
            return response.json()


instagram_publisher = InstagramPublisher()
