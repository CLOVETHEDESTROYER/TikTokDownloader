from typing import Any, Dict, Optional


class DownloaderException(Exception):
    """Base exception for downloader errors"""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        extra: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.extra = extra or {}
        super().__init__(self.message)


class VideoNotFoundError(DownloaderException):
    """Raised when video cannot be found"""

    def __init__(self, url: str):
        super().__init__(
            message=f"Video not found: {url}",
            status_code=404,
            extra={"url": url}
        )


class DownloadError(DownloaderException):
    """Raised when download fails"""

    def __init__(self, url: str, reason: str):
        super().__init__(
            message=f"Failed to download video: {reason}",
            status_code=400,
            extra={"url": url, "reason": reason}
        )


class InvalidURLError(DownloaderException):
    """Raised when URL is invalid"""

    def __init__(self, url: str, platform: str):
        super().__init__(
            message=f"Invalid {platform} URL: {url}",
            status_code=400,
            extra={"url": url, "platform": platform}
        )


class RateLimitExceededError(DownloaderException):
    """Raised when rate limit is exceeded"""

    def __init__(self, retry_after: int):
        super().__init__(
            message="Rate limit exceeded",
            status_code=429,
            extra={"retry_after": retry_after}
        )


class QualityNotAvailableError(DownloaderException):
    """Raised when requested quality is not available"""

    def __init__(self, url: str, quality: str):
        super().__init__(
            message=f"Requested quality {quality} not available",
            status_code=400,
            extra={"url": url, "quality": quality}
        )


class NetworkError(DownloaderException):
    """Raised when network issues occur"""

    def __init__(self, url: str, error: str):
        super().__init__(
            message=f"Network error: {error}",
            status_code=503,
            extra={"url": url, "error": error}
        )


class ValidationError(DownloaderException):
    """Raised when validation fails"""

    def __init__(self, errors: Dict[str, Any]):
        super().__init__(
            message="Validation error",
            status_code=422,
            extra={"errors": errors}
        )
