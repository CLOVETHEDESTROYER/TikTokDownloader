from typing import Any, Dict, Optional
from fastapi import HTTPException


class DownloaderException(HTTPException):
    """Base exception for downloader errors"""

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
        super().__init__(detail=f"Requested quality {quality} not available")


class NetworkError(DownloaderException):
    """Raised when network issues occur"""

    def __init__(self, url: str, error: str):
        super().__init__(detail=f"Network error: {error}")


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


class InvalidURLException(HTTPException):
    def __init__(self, platform: str):
        super().__init__(
            status_code=400,
            detail=f"Invalid {platform} URL provided."
        )


class DownloadFailedException(HTTPException):
    def __init__(self, reason: str):
        super().__init__(
            status_code=500,
            detail=f"Download failed: {reason}"
        )


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid or missing API key"
        )
