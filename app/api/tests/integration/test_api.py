import pytest
from httpx import AsyncClient
from app.models.download import Platform, VideoQuality, DownloadStatus
from app.core.exceptions import VideoNotFoundError


@pytest.mark.asyncio
async def test_health_check(test_client: AsyncClient):
    """Test the health check endpoint."""
    response = await test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_download(test_client: AsyncClient, mock_video_urls: dict):
    """Test creating a new download."""
    response = await test_client.post(
        "/api/v1/downloads",
        json={
            "url": mock_video_urls["tiktok"],
            "platform": Platform.TIKTOK.value,
            "quality": VideoQuality.HIGH.value
        }
    )

    assert response.status_code == 202
    data = response.json()
    assert "session_id" in data
    assert data["status"] == DownloadStatus.PENDING.value
    assert data["progress"] == 0


@pytest.mark.asyncio
async def test_get_download_status(
    test_client: AsyncClient,
    mock_video_urls: dict,
    sample_download_params: dict
):
    """Test retrieving download status."""
    # Create a download first
    create_response = await test_client.post(
        "/api/v1/downloads",
        json=sample_download_params
    )
    session_id = create_response.json()["session_id"]

    # Get status
    response = await test_client.get(f"/api/v1/downloads/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert "status" in data
    assert "progress" in data


@pytest.mark.asyncio
async def test_invalid_url(test_client: AsyncClient):
    """Test handling of invalid URLs."""
    response = await test_client.post(
        "/api/v1/downloads",
        json={
            "url": "not-a-valid-url",
            "platform": Platform.TIKTOK.value,
            "quality": VideoQuality.HIGH.value
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_platform(test_client: AsyncClient, mock_video_urls: dict):
    """Test handling of invalid platform."""
    response = await test_client.post(
        "/api/v1/downloads",
        json={
            "url": mock_video_urls["tiktok"],
            "platform": "invalid-platform",
            "quality": VideoQuality.HIGH.value
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_quality(test_client: AsyncClient, mock_video_urls: dict):
    """Test handling of invalid quality."""
    response = await test_client.post(
        "/api/v1/downloads",
        json={
            "url": mock_video_urls["tiktok"],
            "platform": Platform.TIKTOK.value,
            "quality": "invalid-quality"
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_batch_download(test_client: AsyncClient, mock_video_urls: dict):
    """Test batch download endpoint."""
    urls = [mock_video_urls["tiktok"]] * 3
    response = await test_client.post(
        "/api/v1/downloads/batch",
        json={
            "urls": urls,
            "platform": Platform.TIKTOK.value,
            "quality": VideoQuality.HIGH.value
        }
    )

    assert response.status_code == 202
    data = response.json()
    assert "session_id" in data
    assert data["total_urls"] == 3
    assert data["status"] == DownloadStatus.PENDING.value


@pytest.mark.asyncio
async def test_batch_download_empty_urls(test_client: AsyncClient):
    """Test batch download with empty URL list."""
    response = await test_client.post(
        "/api/v1/downloads/batch",
        json={
            "urls": [],
            "platform": Platform.TIKTOK.value,
            "quality": VideoQuality.HIGH.value
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_download_not_found(test_client: AsyncClient):
    """Test getting status of non-existent download."""
    response = await test_client.get("/api/v1/downloads/non-existent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_rate_limiting(
    test_client: AsyncClient,
    mock_video_urls: dict,
    sample_download_params: dict
):
    """Test rate limiting on the download endpoint."""
    # Make multiple requests in quick succession
    responses = []
    for _ in range(10):  # Adjust based on your rate limit
        response = await test_client.post(
            "/api/v1/downloads",
            json=sample_download_params
        )
        responses.append(response)

    # Check if any requests were rate limited
    assert any(r.status_code == 429 for r in responses)


@pytest.mark.asyncio
async def test_websocket_connection(test_client: AsyncClient):
    """Test WebSocket connection for download progress updates."""
    async with test_client.websocket_connect("/ws/downloads") as websocket:
        # Send a ping message
        await websocket.send_json({"type": "ping"})

        # Receive pong response
        data = await websocket.receive_json()
        assert data["type"] == "pong"
