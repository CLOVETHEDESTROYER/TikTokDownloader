import pytest
from httpx import AsyncClient
from app.main import app
from app.models.download import Platform, VideoQuality


@pytest.fixture(scope="function")
async def test_client():
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_video_urls():
    """Provide mock video URLs for different platforms."""
    return {
        "tiktok": "https://www.tiktok.com/@user/video/1234567890123456789",
        "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "instagram": "https://www.instagram.com/p/ABC123xyz/"
    }


@pytest.fixture
def sample_download_params(mock_video_urls):
    """Provide sample parameters for download requests."""
    return {
        "url": mock_video_urls["tiktok"],
        "platform": Platform.TIKTOK.value,
        "quality": VideoQuality.HIGH.value
    }


@pytest.fixture
def sample_batch_download_params(mock_video_urls):
    """Provide sample parameters for batch download requests."""
    return {
        "urls": [mock_video_urls["tiktok"]] * 3,
        "platform": Platform.TIKTOK.value,
        "quality": VideoQuality.HIGH.value
    }
