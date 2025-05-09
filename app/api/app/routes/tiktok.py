from fastapi import APIRouter, Depends, Header
from typing import Optional, List
from ..models.base import DownloadRequest, BatchDownloadRequest, DownloadResponse, DownloadStatus
from ..core.exceptions import InvalidURLException, DownloadFailedException, UnauthorizedException
from ..services.tiktok import TikTokService
from ..core.config import settings

router = APIRouter(prefix="/api/v1/tiktok", tags=["tiktok"])


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    # Skip API key check in development mode
    if settings.ENV == "development" and not settings.REQUIRE_API_KEY:
        return "dev-mode"

    if not x_api_key or x_api_key != settings.WEBSITE_API_KEY:
        raise UnauthorizedException()
    return x_api_key


@router.post("/download", response_model=DownloadResponse)
async def download_video(
    request: DownloadRequest,
    api_key: str = Depends(verify_api_key)
):
    """Download a single TikTok video"""
    service = TikTokService()
    return await service.download_video(request.url, request.quality)


@router.post("/batch", response_model=List[DownloadResponse])
async def batch_download(
    request: BatchDownloadRequest,
    api_key: str = Depends(verify_api_key)
):
    """Download multiple TikTok videos"""
    service = TikTokService()
    return await service.batch_download(request.urls, request.quality)


@router.get("/status/{session_id}", response_model=DownloadStatus)
async def get_status(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get the status of a download"""
    service = TikTokService()
    return await service.get_status(session_id)
