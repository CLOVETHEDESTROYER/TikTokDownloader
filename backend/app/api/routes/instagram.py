from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Request
from typing import List
from ...models.instagram import (
    InstagramDownloadRequest,
    InstagramDownloadResponse,
    InstagramQuality,
    InstagramMediaType
)
from ...services.instagram import InstagramDownloader
from ...core.exceptions import DownloaderException, DownloadError, InvalidURLError
from ...services.rate_limiter import RateLimiter
from ...core.config import settings
from ...core.error_reporting import ErrorReporter

router = APIRouter(prefix="/instagram", tags=["instagram"])
downloader = InstagramDownloader()
rate_limiter = RateLimiter()


@router.post("/download", response_model=InstagramDownloadResponse)
async def download_instagram_content(
    request: Request,
    download_request: InstagramDownloadRequest,
    background_tasks: BackgroundTasks
):
    """
    Download content from Instagram (posts, reels, stories).

    - **url**: Instagram URL to download from
    - **quality**: Quality of the download (HIGH, MEDIUM, LOW)
    - **include_caption**: Whether to include post caption
    - **include_metadata**: Whether to include additional metadata
    """
    try:
        response = await downloader.download(download_request)
        return response
    except (InvalidURLError, DownloadError) as e:
        ErrorReporter.report_error(
            error_type=type(e).__name__,
            message=str(e),
            context={
                "endpoint": "/instagram/download",
                "request_data": download_request.dict(),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent")
            },
            url=str(download_request.url),
            request_id=getattr(request.state, "request_id", None)
        )
        if isinstance(e, InvalidURLError):
            raise HTTPException(status_code=400, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        ErrorReporter.report_error(
            error_type=type(e).__name__,
            message=str(e),
            context={
                "endpoint": "/instagram/download",
                "request_data": download_request.dict(),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent")
            },
            url=str(download_request.url),
            request_id=getattr(request.state, "request_id", None)
        )
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/batch-download")
async def batch_download_instagram(
    request: Request,
    urls: List[str],
    background_tasks: BackgroundTasks,
    quality: InstagramQuality = InstagramQuality.HIGH
):
    """
    Download multiple Instagram posts/reels/stories at once.

    - **urls**: List of Instagram URLs to download
    - **quality**: Quality setting for all downloads (default: HIGH)
    """
    if len(urls) > settings.MAX_DOWNLOADS:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.MAX_DOWNLOADS} URLs allowed per batch"
        )

    results = []
    for url in urls:
        try:
            download_request = InstagramDownloadRequest(
                url=url, quality=quality)
            result = await downloader.download(download_request)
            results.append({
                "url": url,
                "status": "success",
                "download_url": result.download_url,
                "session_id": result.session_id
            })
        except Exception as e:
            ErrorReporter.report_error(
                error_type=type(e).__name__,
                message=str(e),
                context={
                    "endpoint": "/instagram/batch-download",
                    "url": url,
                    "client_ip": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent")
                },
                url=url,
                request_id=getattr(request.state, "request_id", None)
            )
            results.append({
                "url": url,
                "status": "failed",
                "error": str(e)
            })

    return {"results": results}


@router.get("/validate")
async def validate_instagram_url(request: Request, url: str):
    """
    Validate if a URL is a valid Instagram URL.

    - **url**: Instagram URL to validate
    """
    try:
        from ...services.instagram.utils import validate_instagram_url as validate_url, get_media_type
        is_valid = validate_url(url)
        return {
            "url": url,
            "is_valid": is_valid,
            "media_type": get_media_type(url) if is_valid else None
        }
    except Exception as e:
        ErrorReporter.report_error(
            error_type=type(e).__name__,
            message=str(e),
            context={
                "endpoint": "/instagram/validate",
                "url": url,
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent")
            },
            url=url,
            request_id=getattr(request.state, "request_id", None)
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error validating URL: {str(e)}"
        )
