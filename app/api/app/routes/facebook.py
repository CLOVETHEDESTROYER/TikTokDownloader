from fastapi import APIRouter
from typing import List
from ..models.base import DownloadRequest, BatchDownloadRequest, DownloadResponse, DownloadStatus
from ..models.facebook import FacebookDownloadRequest, FacebookDownloadResponse, FacebookBatchDownloadRequest
from ..services.facebook import FacebookService

router = APIRouter(prefix="/api/v1/facebook", tags=["facebook"])

@router.post("/download", response_model=DownloadResponse)
async def download_video(
    request: DownloadRequest
):
    """Download a single Facebook video"""
    service = FacebookService()
    return await service.download_video(request.url, request.quality)

@router.post("/download-advanced", response_model=FacebookDownloadResponse)
async def download_video_advanced(
    request: FacebookDownloadRequest
):
    """Download Facebook video with advanced options"""
    service = FacebookService()
    result = await service.download_video(request.url, request.quality.value)
    
    return FacebookDownloadResponse(
        url=str(request.url),
        download_url=result["download_url"],
        content_type=result["content_type"],
        metadata=result["metadata"],
        session_id=result["session_id"],
        is_live=result["is_live"]
    )

@router.post("/batch", response_model=List[DownloadResponse])
async def batch_download(
    request: BatchDownloadRequest
):
    """Download multiple Facebook videos"""
    service = FacebookService()
    return await service.batch_download(request.urls, request.quality)

@router.post("/batch-advanced", response_model=List[FacebookDownloadResponse])
async def batch_download_advanced(
    request: FacebookBatchDownloadRequest
):
    """Download multiple Facebook videos with advanced options"""
    service = FacebookService()
    results = await service.batch_download(request.urls, request.quality.value)
    
    # Convert to FacebookDownloadResponse format
    response_list = []
    for result in results:
        if result.get("status") == "completed":
            response_list.append(FacebookDownloadResponse(
                url=result["url"],
                download_url=result["download_url"],
                content_type=result["content_type"],
                metadata=result["metadata"],
                session_id=result["session_id"],
                is_live=result["is_live"]
            ))
    
    return response_list

@router.get("/status/{session_id}", response_model=DownloadStatus)
async def get_status(
    session_id: str
):
    """Get the status of a Facebook download"""
    service = FacebookService()
    return await service.get_status(session_id)

@router.get("/reel-info/{video_id}")
async def get_reel_info(
    video_id: str
):
    """Get information about a Facebook Reel video without downloading"""
    service = FacebookService()
    # This would extract info about a Reel video
    # Implementation would go here
    return {"video_id": video_id, "is_reel": True}
