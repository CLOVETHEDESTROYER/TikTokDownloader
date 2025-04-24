from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import List
from ...models.instagram import (
    InstagramDownloadRequest,
    InstagramDownloadResponse,
    InstagramQuality
)
from ...services.instagram import InstagramDownloader
from ...core.exceptions import DownloadError, InvalidURLError
from ...services.rate_limiter import RateLimiter
from ...core.config import settings

router = APIRouter(prefix="/instagram", tags=["instagram"])
downloader = InstagramDownloader()
rate_limiter = RateLimiter()


@router.post("/download", response_model=InstagramDownloadResponse)
async def download_instagram_content(
    request: InstagramDownloadRequest,
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
        response = await downloader.download(request)
        return response
    except InvalidURLError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DownloadError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/batch-download")
async def batch_download_instagram(
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
            request = InstagramDownloadRequest(url=url, quality=quality)
            result = await downloader.download(request)
            results.append({
                "url": url,
                "status": "success",
                "download_url": result.download_url,
                "session_id": result.session_id
            })
        except Exception as e:
            results.append({
                "url": url,
                "status": "failed",
                "error": str(e)
            })

    return {"results": results}


@router.get("/validate")
async def validate_instagram_url(url: str):
    """
    Validate if a URL is a valid Instagram URL.

    - **url**: Instagram URL to validate
    """
    from ...services.instagram.utils import validate_instagram_url as validate_url, get_media_type
    is_valid = validate_url(url)
    return {
        "url": url,
        "is_valid": is_valid,
        "media_type": get_media_type(url) if is_valid else None
    }
