import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from app.core.config import settings
from app.models.social import ContentItem, DownloadQueue, ContentStatus
from app.core.exceptions import DownloadFailedException

logger = logging.getLogger(__name__)


class DownloadQueueService:
    def __init__(self):
        self.queue: List[DownloadQueue] = []
        self.active_downloads: Dict[str, Dict[str, Any]] = {}
        self.download_path = settings.DOWNLOAD_FOLDER

    async def add_to_queue(self, content_item: ContentItem, priority: int = 0) -> str:
        """Add content item to download queue"""
        queue_item = DownloadQueue(
            content_item_id=content_item.id,
            priority=priority,
            status="pending"
        )
        
        # Insert based on priority (higher priority first)
        inserted = False
        for i, item in enumerate(self.queue):
            if priority > item.priority:
                self.queue.insert(i, queue_item)
                inserted = True
                break
        
        if not inserted:
            self.queue.append(queue_item)
        
        logger.info(f"Added content {content_item.id} to download queue with priority {priority}")
        return queue_item.id

    async def process_queue(self):
        """Process the download queue"""
        while self.queue:
            # Get highest priority item
            queue_item = self.queue.pop(0)
            
            try:
                await self._process_download(queue_item)
            except Exception as e:
                logger.error(f"Failed to process download {queue_item.id}: {e}")
                queue_item.status = "failed"
                queue_item.error_message = str(e)
                queue_item.retry_count += 1
                
                # Retry if under retry limit
                if queue_item.retry_count < 3:
                    queue_item.status = "pending"
                    self.queue.append(queue_item)
                    logger.info(f"Retrying download {queue_item.id} (attempt {queue_item.retry_count})")

    async def _process_download(self, queue_item: DownloadQueue):
        """Process a single download"""
        queue_item.status = "downloading"
        queue_item.started_at = datetime.utcnow()
        
        try:
            # Get content item (in real implementation, this would query database)
            content_item = await self._get_content_item(queue_item.content_item_id)
            if not content_item:
                raise DownloadFailedException("Content item not found")
            
            # Update content status
            content_item.status = ContentStatus.DOWNLOADING
            content_item.updated_at = datetime.utcnow()
            
            # Download based on platform
            if content_item.platform == "instagram":
                await self._download_instagram_content(content_item)
            elif content_item.platform == "tiktok":
                await self._download_tiktok_content(content_item)
            elif content_item.platform == "facebook":
                await self._download_facebook_content(content_item)
            elif content_item.platform == "youtube":
                await self._download_youtube_content(content_item)
            else:
                raise DownloadFailedException(f"Unsupported platform: {content_item.platform}")
            
            # Update status
            queue_item.status = "completed"
            queue_item.completed_at = datetime.utcnow()
            content_item.status = ContentStatus.DOWNLOADED
            content_item.updated_at = datetime.utcnow()
            
            logger.info(f"Successfully downloaded content {content_item.id}")
            
        except Exception as e:
            queue_item.status = "failed"
            queue_item.error_message = str(e)
            queue_item.completed_at = datetime.utcnow()
            
            if content_item:
                content_item.status = ContentStatus.FAILED
                content_item.updated_at = datetime.utcnow()
            
            raise

    async def _download_instagram_content(self, content_item: ContentItem):
        """Download Instagram content"""
        # This would use your existing Instagram download logic
        # For now, just simulate the download
        logger.info(f"Downloading Instagram content: {content_item.original_url}")
        
        # Simulate download time
        await asyncio.sleep(2)
        
        # In real implementation, you would:
        # 1. Use yt-dlp to download the content
        # 2. Remove watermarks if needed
        # 3. Save to the downloads folder
        # 4. Update the content item with file path
        
        content_item.metadata = {
            **(content_item.metadata or {}),
            "download_path": f"{self.download_path}/instagram_{uuid.uuid4().hex[:8]}.mp4",
            "download_timestamp": datetime.utcnow().isoformat()
        }

    async def _download_tiktok_content(self, content_item: ContentItem):
        """Download TikTok content"""
        logger.info(f"Downloading TikTok content: {content_item.original_url}")
        await asyncio.sleep(2)
        
        content_item.metadata = {
            **(content_item.metadata or {}),
            "download_path": f"{self.download_path}/tiktok_{uuid.uuid4().hex[:8]}.mp4",
            "download_timestamp": datetime.utcnow().isoformat()
        }

    async def _download_facebook_content(self, content_item: ContentItem):
        """Download Facebook content"""
        logger.info(f"Downloading Facebook content: {content_item.original_url}")
        await asyncio.sleep(2)
        
        content_item.metadata = {
            **(content_item.metadata or {}),
            "download_path": f"{self.download_path}/facebook_{uuid.uuid4().hex[:8]}.mp4",
            "download_timestamp": datetime.utcnow().isoformat()
        }

    async def _download_youtube_content(self, content_item: ContentItem):
        """Download YouTube content"""
        logger.info(f"Downloading YouTube content: {content_item.original_url}")
        await asyncio.sleep(2)
        
        content_item.metadata = {
            **(content_item.metadata or {}),
            "download_path": f"{self.download_path}/youtube_{uuid.uuid4().hex[:8]}.mp4",
            "download_timestamp": datetime.utcnow().isoformat()
        }

    async def _get_content_item(self, content_id: str) -> Optional[ContentItem]:
        """Get content item by ID (mock implementation)"""
        # In real implementation, this would query the database
        return ContentItem(
            id=content_id,
            source_account_id="mock_account",
            original_url="https://example.com/mock",
            platform="instagram",
            content_type="reel",
            status=ContentStatus.COLLECTED
        )

    async def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "queue_length": len(self.queue),
            "active_downloads": len(self.active_downloads),
            "pending_items": len([item for item in self.queue if item.status == "pending"]),
            "failed_items": len([item for item in self.queue if item.status == "failed"]),
            "queue_items": [
                {
                    "id": item.id,
                    "content_item_id": item.content_item_id,
                    "priority": item.priority,
                    "status": item.status,
                    "retry_count": item.retry_count,
                    "created_at": item.created_at.isoformat()
                }
                for item in self.queue
            ]
        }

    async def clear_failed_items(self):
        """Clear all failed items from queue"""
        self.queue = [item for item in self.queue if item.status != "failed"]
        logger.info("Cleared failed items from download queue")

    async def start_background_processor(self):
        """Start the background queue processor"""
        logger.info("Starting download queue background processor")
        
        while True:
            try:
                if self.queue:
                    await self.process_queue()
                else:
                    # Wait a bit before checking again
                    await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"Error in queue processor: {e}")
                await asyncio.sleep(10)  # Wait longer on error


# Global instance
download_queue_service = DownloadQueueService()
