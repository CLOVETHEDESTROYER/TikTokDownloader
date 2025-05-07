from fastapi import APIRouter, Depends, Header
from typing import Optional, List
from ..models.base import DownloadRequest, BatchDownloadRequest, DownloadResponse, DownloadStatus
from ..core.exceptions import InvalidURLException, DownloadFailedException, UnauthorizedException
from ..services.instagram import InstagramService
from ..core.config import settings

router = APIRouter(prefix="/api/v1/instagram", tags=["instagram"])

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.WEBSITE_API_KEY:
        raise UnauthorizedException()
    return x_api_key

@router.post("/download", response_model=DownloadResponse)
async def download_content(
    request: DownloadRequest,
    api_key: str = Depends(verify_api_key)
):
    """Download Instagram content (post, reel, or story)"""
    service = InstagramService()
    return await service.download_content(request.url, request.quality)

@router.post("/batch", response_model=List[DownloadResponse])
async def batch_download(
    request: BatchDownloadRequest,
    api_key: str = Depends(verify_api_key)
):
    """Download multiple Instagram posts"""
    service = InstagramService()
    return await service.batch_download(request.urls, request.quality)

@router.get("/status/{session_id}", response_model=DownloadStatus)
async def get_status(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get the status of a download"""
    service = InstagramService()
    return await service.get_status(session_id) 