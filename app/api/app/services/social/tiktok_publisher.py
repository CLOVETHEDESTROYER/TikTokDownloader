import httpx
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from app.core.config import settings
from app.models.social import SocialAccount, ContentItem, ScheduledPost, ContentStatus

logger = logging.getLogger(__name__)


class TikTokPublisher:
    def __init__(self):
        self.api_base_url = "https://open-api.tiktok.com"
        self.upload_url = f"{self.api_base_url}/share/video/upload/"
        
    async def publish_video(
        self, 
        account: SocialAccount, 
        content_item: ContentItem, 
        video_path: str,
        caption: str = "",
        hashtags: list = None,
        privacy_level: str = "PUBLIC_TO_EVERYONE"
    ) -> Dict[str, Any]:
        """
        Publish a video to TikTok using the TikTok for Developers API.
        
        Args:
            account: TikTok social account with access token
            content_item: Content item being published
            video_path: Local path to the video file
            caption: Video caption/description
            hashtags: List of hashtags to include
            privacy_level: Privacy setting for the video
            
        Returns:
            Dict containing publish result and video ID
        """
        try:
            logger.info(f"Starting TikTok video publish for content {content_item.id}")
            
            # Prepare hashtags
            if hashtags:
                hashtag_string = " ".join([f"#{tag}" for tag in hashtags])
                full_caption = f"{caption}\n\n{hashtag_string}".strip()
            else:
                full_caption = caption
                
            # Step 1: Initialize upload
            upload_init_response = await self._initialize_upload(account.access_token)
            if not upload_init_response.get('success'):
                raise Exception(f"Failed to initialize upload: {upload_init_response.get('error')}")
                
            upload_url = upload_init_response['data']['upload_url']
            publish_id = upload_init_response['data']['publish_id']
            
            # Step 2: Upload video file
            upload_result = await self._upload_video_file(upload_url, video_path)
            if not upload_result.get('success'):
                raise Exception(f"Failed to upload video file: {upload_result.get('error')}")
                
            # Step 3: Publish video
            publish_result = await self._publish_video(
                account.access_token,
                publish_id,
                full_caption,
                privacy_level
            )
            
            if publish_result.get('success'):
                logger.info(f"Successfully published TikTok video for content {content_item.id}")
                return {
                    "success": True,
                    "platform": "tiktok",
                    "video_id": publish_result['data'].get('video_id'),
                    "publish_id": publish_id,
                    "published_at": datetime.now().isoformat(),
                    "caption": full_caption
                }
            else:
                raise Exception(f"Failed to publish video: {publish_result.get('error')}")
                
        except Exception as e:
            logger.error(f"TikTok publish failed for content {content_item.id}: {str(e)}")
            return {
                "success": False,
                "platform": "tiktok",
                "error": str(e),
                "content_id": content_item.id
            }
    
    async def _initialize_upload(self, access_token: str) -> Dict[str, Any]:
        """Initialize video upload with TikTok API."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}/share/video/upload/",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "source_info": {
                        "source": "FILE_UPLOAD",
                        "video_size": 0,  # Will be updated after file upload
                        "chunk_size": 0,
                        "total_chunk_count": 1
                    }
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def _upload_video_file(self, upload_url: str, video_path: str) -> Dict[str, Any]:
        """Upload video file to TikTok's servers."""
        try:
            with open(video_path, 'rb') as video_file:
                async with httpx.AsyncClient() as client:
                    response = await client.put(
                        upload_url,
                        content=video_file.read(),
                        headers={"Content-Type": "video/mp4"}
                    )
                    response.raise_for_status()
                    return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _publish_video(
        self, 
        access_token: str, 
        publish_id: str, 
        caption: str, 
        privacy_level: str
    ) -> Dict[str, Any]:
        """Publish the uploaded video."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}/share/video/publish/",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "publish_id": publish_id,
                    "post_info": {
                        "title": caption,
                        "privacy_level": privacy_level,
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False,
                        "video_cover_timestamp_ms": 1000
                    }
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def get_video_status(self, access_token: str, video_id: str) -> Dict[str, Any]:
        """Get the status of a published video."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_base_url}/share/video/query/",
                headers={"Authorization": f"Bearer {access_token}"},
                params={"video_id": video_id}
            )
            response.raise_for_status()
            return response.json()
    
    async def delete_video(self, access_token: str, video_id: str) -> Dict[str, Any]:
        """Delete a published video."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}/share/video/delete/",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={"video_id": video_id}
            )
            response.raise_for_status()
            return response.json()


tiktok_publisher = TikTokPublisher()
