import pytest
from unittest.mock import Mock, patch
from ...app.services.download_manager import DownloadManager
from ...app.models.download import Platform, VideoQuality, DownloadStatus
from ...app.core.exceptions import (
    VideoNotFoundError,
    QualityNotAvailableError,
    NetworkError,
    DownloadError
)

pytestmark = pytest.mark.asyncio


async def test_create_download(download_manager: DownloadManager, mock_video_urls: dict):
    """Test creating a new download session."""
    session_id = await download_manager.create_download(
        mock_video_urls["tiktok"],
        Platform.TIKTOK
    )

    assert session_id is not None
    assert session_id in download_manager.active_downloads
    assert download_manager.active_downloads[session_id]["status"] == DownloadStatus.PENDING
    assert download_manager.active_downloads[session_id]["progress"] == 0


async def test_get_download_status(download_manager: DownloadManager, mock_video_urls: dict):
    """Test retrieving download status."""
    # Create a download first
    session_id = await download_manager.create_download(
        mock_video_urls["tiktok"],
        Platform.TIKTOK
    )

    # Get status
    status = await download_manager.get_download_status(session_id)
    assert status is not None
    assert status.session_id == session_id
    assert status.status == DownloadStatus.PENDING
    assert status.progress == 0


async def test_invalid_session_id(download_manager: DownloadManager):
    """Test handling of invalid session IDs."""
    status = await download_manager.get_download_status("invalid-session")
    assert status is None


@patch('yt_dlp.YoutubeDL')
async def test_process_download_success(
    mock_ydl,
    download_manager: DownloadManager,
    mock_video_urls: dict,
    mock_video_info: dict
):
    """Test successful video download processing."""
    # Mock YoutubeDL behavior
    mock_ydl.return_value.extract_info.return_value = mock_video_info

    # Create download session
    session_id = await download_manager.create_download(
        mock_video_urls["tiktok"],
        Platform.TIKTOK
    )

    # Process download
    response = await download_manager.process_download(
        session_id,
        mock_video_urls["tiktok"],
        Platform.TIKTOK,
        VideoQuality.HIGH
    )

    assert response.status == DownloadStatus.COMPLETED
    assert response.progress == 100
    assert response.filename is not None


@patch('yt_dlp.YoutubeDL')
async def test_video_not_found(
    mock_ydl,
    download_manager: DownloadManager,
    mock_video_urls: dict
):
    """Test handling of non-existent videos."""
    # Mock video not found
    mock_ydl.return_value.extract_info.return_value = None

    session_id = await download_manager.create_download(
        mock_video_urls["tiktok_invalid"],
        Platform.TIKTOK
    )

    with pytest.raises(VideoNotFoundError):
        await download_manager.process_download(
            session_id,
            mock_video_urls["tiktok_invalid"],
            Platform.TIKTOK,
            VideoQuality.HIGH
        )


@patch('yt_dlp.YoutubeDL')
async def test_quality_not_available(
    mock_ydl,
    download_manager: DownloadManager,
    mock_video_urls: dict
):
    """Test handling of unavailable video quality."""
    # Mock video info with only low quality available
    mock_ydl.return_value.extract_info.return_value = {
        "formats": [{"height": 360}]  # Only low quality available
    }

    session_id = await download_manager.create_download(
        mock_video_urls["tiktok"],
        Platform.TIKTOK
    )

    with pytest.raises(QualityNotAvailableError):
        await download_manager.process_download(
            session_id,
            mock_video_urls["tiktok"],
            Platform.TIKTOK,
            VideoQuality.HIGH
        )


@patch('yt_dlp.YoutubeDL')
async def test_network_error(
    mock_ydl,
    download_manager: DownloadManager,
    mock_video_urls: dict
):
    """Test handling of network errors."""
    # Mock network error
    mock_ydl.return_value.extract_info.side_effect = Exception(
        "Network timeout")

    session_id = await download_manager.create_download(
        mock_video_urls["tiktok"],
        Platform.TIKTOK
    )

    with pytest.raises(NetworkError):
        await download_manager.process_download(
            session_id,
            mock_video_urls["tiktok"],
            Platform.TIKTOK,
            VideoQuality.HIGH
        )


@patch('yt_dlp.YoutubeDL')
async def test_batch_download(
    mock_ydl,
    download_manager: DownloadManager,
    mock_video_urls: dict,
    mock_video_info: dict
):
    """Test batch download processing."""
    # Mock successful video info extraction
    mock_ydl.return_value.extract_info.return_value = mock_video_info

    urls = [mock_video_urls["tiktok"]] * 3  # Test with 3 URLs
    session_id = await download_manager.create_download(
        urls[0],
        Platform.TIKTOK
    )

    response = await download_manager.process_batch_download(
        session_id,
        urls,
        Platform.TIKTOK,
        VideoQuality.HIGH
    )

    assert response.total_urls == 3
    assert response.processed_urls == 3
    assert response.status == DownloadStatus.COMPLETED
    assert response.progress == 100


@patch('yt_dlp.YoutubeDL')
async def test_batch_download_partial_failure(
    mock_ydl,
    download_manager: DownloadManager,
    mock_video_urls: dict,
    mock_video_info: dict
):
    """Test batch download with some failures."""
    def mock_extract_info(url, download=False):
        if "invalid" in url:
            raise Exception("Download failed")
        return mock_video_info

    mock_ydl.return_value.extract_info.side_effect = mock_extract_info

    urls = [
        mock_video_urls["tiktok"],
        mock_video_urls["tiktok_invalid"],
        mock_video_urls["tiktok"]
    ]

    session_id = await download_manager.create_download(
        urls[0],
        Platform.TIKTOK
    )

    response = await download_manager.process_batch_download(
        session_id,
        urls,
        Platform.TIKTOK,
        VideoQuality.HIGH
    )

    assert response.total_urls == 3
    assert response.processed_urls == 3
    # Failed because of partial failure
    assert response.status == DownloadStatus.FAILED
    assert "errors" in download_manager.active_downloads[session_id]
    assert len(download_manager.active_downloads[session_id]["errors"]) == 1
