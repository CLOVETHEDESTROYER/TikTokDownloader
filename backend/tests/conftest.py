import pytest
import asyncio
from typing import Generator, AsyncGenerator
import tempfile
import shutil
import os
from app.main import app
from app.models.download import Platform, VideoQuality
from app.services.download_manager import DownloadManager


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def download_manager() -> AsyncGenerator[DownloadManager, None]:
    """Create a test instance of DownloadManager."""
    manager = DownloadManager()
    # Use a temporary directory for downloads
    manager.download_folder = tempfile.mkdtemp()
    yield manager
    # Cleanup after tests
    shutil.rmtree(manager.download_folder)


@pytest.fixture
def mock_video_urls() -> dict:
    """Sample video URLs for testing."""
    return {
        "tiktok": "https://www.tiktok.com/@user/video/1234567890",
        "tiktok_invalid": "https://www.tiktok.com/invalid",
        "instagram": "https://www.instagram.com/p/abcdef123456/",
        "instagram_invalid": "https://www.instagram.com/invalid",
        "non_platform": "https://example.com/video"
    }


@pytest.fixture
def mock_video_info() -> dict:
    """Sample video information for testing."""
    return {
        "title": "Test Video",
        "formats": [
            {"format_id": "1080p", "height": 1080},
            {"format_id": "720p", "height": 720},
            {"format_id": "480p", "height": 480}
        ],
        "duration": 30,
        "view_count": 1000,
        "like_count": 100
    }


@pytest.fixture
def sample_download_params() -> dict:
    """Sample download parameters for testing."""
    return {
        "url": "https://www.tiktok.com/@user/video/1234567890",
        "platform": Platform.TIKTOK,
        "quality": VideoQuality.HIGH
    }
