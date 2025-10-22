import asyncio
import logging
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.models.social import (
    SocialAccount, 
    ContentItem, 
    ScheduledPost, 
    ContentStatus,
    SocialPlatform
)
from app.services.social.tiktok_publisher import tiktok_publisher
from app.services.social.instagram_publisher import instagram_publisher

logger = logging.getLogger(__name__)


class PublishingManager:
    def __init__(self):
        self.active_publishes: Dict[str, asyncio.Task] = {}
        self.max_concurrent_publishes = 2
        
    async def schedule_post(
        self,
        content_item: ContentItem,
        target_platforms: List[SocialPlatform],
        scheduled_time: datetime,
        caption: str = "",
        hashtags: List[str] = None,
        **kwargs
    ) -> str:
        """
        Schedule a post for publishing at a specific time.
        
        Args:
            content_item: Content item to publish
            target_platforms: List of platforms to publish to
            scheduled_time: When to publish the content
            caption: Post caption
            hashtags: List of hashtags
            **kwargs: Additional platform-specific options
            
        Returns:
            Scheduled post ID
        """
        scheduled_post = ScheduledPost(
            content_item_id=content_item.id,
            target_platforms=target_platforms,
            scheduled_time=scheduled_time,
            post_data={
                "caption": caption,
                "hashtags": hashtags or [],
                "kwargs": kwargs
            }
        )
        
        # In a real implementation, this would be saved to database
        logger.info(f"Scheduled post {scheduled_post.id} for {scheduled_time}")
        
        # Start the scheduling task
        asyncio.create_task(self._process_scheduled_post(scheduled_post))
        
        return scheduled_post.id
    
    async def publish_now(
        self,
        content_item: ContentItem,
        target_platforms: List[SocialPlatform],
        accounts: Dict[SocialPlatform, SocialAccount],
        caption: str = "",
        hashtags: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Publish content immediately to specified platforms.
        
        Args:
            content_item: Content item to publish
            target_platforms: List of platforms to publish to
            accounts: Mapping of platform to social account
            caption: Post caption
            hashtags: List of hashtags
            **kwargs: Additional platform-specific options
            
        Returns:
            Dict containing publish results for each platform
        """
        if not content_item.download_path or not os.path.exists(content_item.download_path):
            return {
                "success": False,
                "error": "Content not downloaded or file not found",
                "content_id": content_item.id
            }
        
        results = {}
        
        for platform in target_platforms:
            if platform not in accounts:
                results[platform] = {
                    "success": False,
                    "error": f"No account found for platform {platform}"
                }
                continue
                
            account = accounts[platform]
            
            try:
                if platform == SocialPlatform.TIKTOK:
                    result = await tiktok_publisher.publish_video(
                        account=account,
                        content_item=content_item,
                        video_path=content_item.download_path,
                        caption=caption,
                        hashtags=hashtags,
                        privacy_level=kwargs.get('privacy_level', 'PUBLIC_TO_EVERYONE')
                    )
                elif platform == SocialPlatform.INSTAGRAM:
                    result = await instagram_publisher.publish_video(
                        account=account,
                        content_item=content_item,
                        video_path=content_item.download_path,
                        caption=caption,
                        hashtags=hashtags,
                        location_id=kwargs.get('location_id')
                    )
                else:
                    result = {
                        "success": False,
                        "error": f"Publishing not supported for platform {platform}"
                    }
                
                results[platform] = result
                
                if result.get('success'):
                    logger.info(f"Successfully published to {platform} for content {content_item.id}")
                else:
                    logger.error(f"Failed to publish to {platform}: {result.get('error')}")
                    
            except Exception as e:
                logger.error(f"Exception during {platform} publish: {str(e)}")
                results[platform] = {
                    "success": False,
                    "error": str(e),
                    "platform": platform
                }
        
        # Check if all publishes were successful
        all_successful = all(result.get('success', False) for result in results.values())
        
        return {
            "success": all_successful,
            "content_id": content_item.id,
            "platforms": results,
            "published_at": datetime.now().isoformat()
        }
    
    async def _process_scheduled_post(self, scheduled_post: ScheduledPost):
        """Process a scheduled post when its time comes."""
        try:
            # Wait until scheduled time
            wait_time = (scheduled_post.scheduled_time - datetime.now()).total_seconds()
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            
            logger.info(f"Processing scheduled post {scheduled_post.id}")
            
            # In a real implementation, we would:
            # 1. Fetch the content item from database
            # 2. Get the associated social accounts
            # 3. Call publish_now with the scheduled post data
            
            # For now, just log the scheduled post
            logger.info(f"Would publish scheduled post {scheduled_post.id} to {scheduled_post.target_platforms}")
            
        except Exception as e:
            logger.error(f"Error processing scheduled post {scheduled_post.id}: {str(e)}")
    
    async def get_publish_status(self, content_id: str) -> Dict[str, Any]:
        """Get the publishing status for a content item."""
        # In a real implementation, this would query the database
        return {
            "content_id": content_id,
            "status": "unknown",
            "published_platforms": [],
            "scheduled_posts": [],
            "last_updated": datetime.now().isoformat()
        }
    
    async def cancel_scheduled_post(self, scheduled_post_id: str) -> bool:
        """Cancel a scheduled post."""
        # In a real implementation, this would update the database
        logger.info(f"Cancelled scheduled post {scheduled_post_id}")
        return True
    
    async def delete_published_content(
        self, 
        content_id: str, 
        platform: SocialPlatform,
        account: SocialAccount,
        media_id: str
    ) -> Dict[str, Any]:
        """Delete published content from a platform."""
        try:
            if platform == SocialPlatform.TIKTOK:
                result = await tiktok_publisher.delete_video(account.access_token, media_id)
            elif platform == SocialPlatform.INSTAGRAM:
                result = await instagram_publisher.delete_media(account.access_token, media_id)
            else:
                return {"success": False, "error": f"Deletion not supported for {platform}"}
            
            if result.get('success', False):
                logger.info(f"Successfully deleted {platform} content {media_id}")
            else:
                logger.error(f"Failed to delete {platform} content: {result}")
                
            return result
            
        except Exception as e:
            logger.error(f"Exception during {platform} content deletion: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def cleanup_after_publish(self, content_item: ContentItem) -> bool:
        """Clean up local files after successful publishing."""
        try:
            if content_item.download_path and os.path.exists(content_item.download_path):
                os.remove(content_item.download_path)
                logger.info(f"Cleaned up file {content_item.download_path} after publishing")
                return True
        except Exception as e:
            logger.error(f"Failed to cleanup file {content_item.download_path}: {str(e)}")
        return False


publishing_manager = PublishingManager()
