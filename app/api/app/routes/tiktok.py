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


@router.post("/download")
async def download_video(url: str, api_key: str = Depends(verify_api_key)):
    """Download a single TikTok video"""
    service = TikTokService()
    try:
        result = await service.download_video(url)
        return {
            "status": "success",
            "filename": result["filename"],
            "title": result["title"],
            "url": result["url"]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/batch")
async def batch_download(urls: List[str], api_key: str = Depends(verify_api_key)):
    """Download multiple TikTok videos"""
    service = TikTokService()
    try:
        results = await service.batch_download(urls)
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/status/{session_id}", response_model=DownloadStatus)
async def get_status(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get the status of a download"""
    service = TikTokService()
    return await service.get_status(session_id)
