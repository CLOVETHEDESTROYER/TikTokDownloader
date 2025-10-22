from typing import Any, Dict, Optional
from fastapi import HTTPException


class DownloaderException(HTTPException):
    """Base exception for the downloader application"""

    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class VideoNotFoundError(DownloaderException):
    """Raised when video cannot be found"""

    def __init__(self, url: str):
        super().__init__(detail=f"Video not found: {url}")


class DownloadError(DownloaderException):
    """Raised when download fails"""

    def __init__(self, url: str, reason: str):
        super().__init__(detail=f"Failed to download video: {reason}")


class InvalidURLError(DownloaderException):
    """Raised when URL is invalid"""

    def __init__(self, url: str, platform: str):
        super().__init__(detail=f"Invalid {platform} URL: {url}")


class RateLimitExceededError(DownloaderException):
    """Raised when rate limit is exceeded"""

    def __init__(self):
        super().__init__(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )


class QualityNotAvailableError(DownloaderException):
    """Raised when requested quality is not available"""

    def __init__(self, url: str, quality: str):
        super().__init__(
            detail=f"Quality '{quality}' not available for video {url}")


class NetworkError(DownloaderException):
    """Raised when network issues occur"""

    def __init__(self, url: str, reason: str):
        super().__init__(detail=f"Network error downloading {url}: {reason}")


class ValidationError(DownloaderException):
    """Raised when validation fails"""

    def __init__(self, errors: Dict[str, Any]):
        super().__init__(
            status_code=422,
            detail={"errors": errors}
        )


class RateLimitException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )


class InvalidURLException(DownloaderException):
    """Raised when URL is invalid for TikTok service"""

    def __init__(self, reason: str):
        super().__init__(detail=f"Invalid URL: {reason}")


class DownloadFailedException(DownloaderException):
    """Raised when download fails for TikTok service"""

    def __init__(self, reason: str):
        super().__init__(detail=f"Download failed: {reason}")


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Invalid or missing API key"):
        super().__init__(
            status_code=401,
            detail=detail
        )
