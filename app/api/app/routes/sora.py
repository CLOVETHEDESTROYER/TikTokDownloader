from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import logging

from ..services.sora import SoraService
from ..core.exceptions import DownloadFailedException, InvalidURLException

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sora", tags=["sora"])

# Initialize Sora service
sora_service = SoraService()


class SoraDownloadRequest(BaseModel):
    url: HttpUrl
    quality: str = "high"
    cookies: Optional[str] = None


class SoraBatchDownloadRequest(BaseModel):
    urls: List[HttpUrl]
    quality: str = "high"


class SoraTestRequest(BaseModel):
    url: HttpUrl
    cookies: Optional[str] = None


@router.post("/download")
async def download_sora_video(request: SoraDownloadRequest):
    """
    Download a single Sora video without watermark
    """
    try:
        result = await sora_service.download_video(str(request.url), request.quality, request.cookies)
        return result
    except DownloadFailedException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidURLException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error downloading Sora video: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/batch")
async def batch_download_sora_videos(request: SoraBatchDownloadRequest):
    """
    Download multiple Sora videos
    """
    try:
        url_strings = [str(url) for url in request.urls]
        results = await sora_service.batch_download(url_strings, request.quality)
        return {"results": results}
    except Exception as e:
        logger.error(f"Unexpected error in batch download: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/test")
async def test_sora_extraction(request: SoraTestRequest):
    """
    Test Sora video extraction to see available formats
    This is useful for debugging and understanding what yt-dlp can extract
    """
    try:
        result = await sora_service.test_sora_extraction(str(request.url), request.cookies)
        return result
    except Exception as e:
        logger.error(f"Error testing Sora extraction: {str(e)}")
        return {
            "url": str(request.url),
            "error": str(e),
            "formats": [],
            "extractor": "Failed"
        }


@router.get("/status/{session_id}")
async def get_sora_download_status(session_id: str):
    """
    Get the status of a Sora download
    """
    try:
        status = await sora_service.get_status(session_id)
        return status
    except Exception as e:
        logger.error(f"Error getting Sora download status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def sora_health_check():
    """
    Health check for Sora service
    """
    return {
        "status": "healthy",
        "service": "sora",
        "watermark_removal_enabled": sora_service.force_no_watermark
    }
