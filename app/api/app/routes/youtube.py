from fastapi import APIRouter, Depends, Header
from typing import Optional, List
from ..models.base import DownloadRequest, BatchDownloadRequest, DownloadResponse, DownloadStatus
from ..models.youtube import YouTubeDownloadRequest, YouTubeDownloadResponse, YouTubeBatchDownloadRequest
from ..core.exceptions import InvalidURLException, DownloadFailedException, UnauthorizedException
from ..services.youtube import YouTubeService
from ..core.config import settings

router = APIRouter(prefix="/api/v1/youtube", tags=["youtube"])

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.WEBSITE_API_KEY:
        raise UnauthorizedException()
    return x_api_key

@router.post("/download", response_model=DownloadResponse)
async def download_video(
    request: DownloadRequest,
    api_key: str = Depends(verify_api_key)
):
    """Download a single YouTube video or Short"""
    service = YouTubeService()
    return await service.download_video(request.url, request.quality)

@router.post("/download-advanced", response_model=YouTubeDownloadResponse)
async def download_video_advanced(
    request: YouTubeDownloadRequest,
    api_key: str = Depends(verify_api_key)
):
    """Download YouTube video/Shorts with advanced options"""
    service = YouTubeService()
    result = await service.download_video(request.url, request.quality.value)
    
    # Convert to YouTubeDownloadResponse format
    return YouTubeDownloadResponse(
        url=str(request.url),
        download_url=result["download_url"],
        content_type=result["content_type"],
        metadata=result["metadata"],
        session_id=result["session_id"],
        is_shorts=result["is_shorts"]
    )

@router.post("/batch", response_model=List[DownloadResponse])
async def batch_download(
    request: BatchDownloadRequest,
    api_key: str = Depends(verify_api_key)
):
    """Download multiple YouTube videos/Shorts"""
    service = YouTubeService()
    return await service.batch_download(request.urls, request.quality)

@router.post("/batch-advanced", response_model=List[YouTubeDownloadResponse])
async def batch_download_advanced(
    request: YouTubeBatchDownloadRequest,
    api_key: str = Depends(verify_api_key)
):
    """Download multiple YouTube videos/Shorts with advanced options"""
    service = YouTubeService()
    results = await service.batch_download(request.urls, request.quality.value)
    
    # Convert to YouTubeDownloadResponse format
    response_list = []
    for result in results:
        if result.get("status") == "completed":
            response_list.append(YouTubeDownloadResponse(
                url=result["url"],
                download_url=result["download_url"],
                content_type=result["content_type"],
                metadata=result["metadata"],
                session_id=result["session_id"],
                is_shorts=result["is_shorts"]
            ))
    
    return response_list

@router.get("/status/{session_id}", response_model=DownloadStatus)
async def get_status(
    session_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get the status of a YouTube download"""
    service = YouTubeService()
    return await service.get_status(session_id)

@router.get("/shorts-info/{video_id}")
async def get_shorts_info(
    video_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get information about a YouTube Shorts video without downloading"""
    service = YouTubeService()
    # This would extract info about a Shorts video
    # Implementation would go here
    return {"video_id": video_id, "is_shorts": True}
