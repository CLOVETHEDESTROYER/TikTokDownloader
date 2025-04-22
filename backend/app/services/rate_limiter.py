from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from enum import Enum
import time


class UserTier(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class RateLimitConfig:
    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
        bulk_download_limit: int,
        download_limit: int
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.bulk_download_limit = bulk_download_limit
        self.download_limit = download_limit


class RateLimiter:
    def __init__(self):
        # Store request counts and timestamps per IP/user
        self.requests: Dict[str, list] = {}
        # Store bulk download counts per IP/user
        self.bulk_downloads: Dict[str, list] = {}
        # Store single download counts per IP/user
        self.downloads: Dict[str, list] = {}

        # Configure limits for different tiers
        self.tier_configs = {
            UserTier.FREE: RateLimitConfig(
                max_requests=100,  # 100 requests per 30 minutes
                window_seconds=1800,  # 30 minutes window
                bulk_download_limit=5,  # 5 bulk downloads per 30 minutes
                download_limit=5  # 5 downloads per 30 minutes for free users
            ),
            UserTier.PREMIUM: RateLimitConfig(
                max_requests=500,
                window_seconds=3600,
                bulk_download_limit=20,
                download_limit=100  # 100 downloads per hour for premium users
            ),
            UserTier.ENTERPRISE: RateLimitConfig(
                max_requests=2000,
                window_seconds=3600,
                bulk_download_limit=100,
                download_limit=500  # 500 downloads per hour for enterprise users
            )
        }

    def _clean_old_requests(self, key: str, window_seconds: int) -> None:
        """Remove requests older than the window."""
        if key in self.requests:
            current_time = time.time()
            self.requests[key] = [
                timestamp for timestamp in self.requests[key]
                if current_time - timestamp < window_seconds
            ]

    def _clean_old_bulk_downloads(self, key: str, window_seconds: int) -> None:
        """Remove bulk downloads older than the window."""
        if key in self.bulk_downloads:
            current_time = time.time()
            self.bulk_downloads[key] = [
                timestamp for timestamp in self.bulk_downloads[key]
                if current_time - timestamp < window_seconds
            ]

    def _clean_old_downloads(self, key: str, window_seconds: int) -> None:
        """Remove downloads older than the window."""
        if key in self.downloads:
            current_time = time.time()
            self.downloads[key] = [
                timestamp for timestamp in self.downloads[key]
                if current_time - timestamp < window_seconds
            ]

    def is_rate_limited(self, key: str, tier: UserTier = UserTier.FREE) -> Tuple[bool, Optional[int]]:
        """
        Check if a request should be rate limited.
        Returns (is_limited, retry_after_seconds)
        """
        config = self.tier_configs[tier]
        current_time = time.time()

        # Clean old requests
        self._clean_old_requests(key, config.window_seconds)

        # Initialize request list if not exists
        if key not in self.requests:
            self.requests[key] = []

        # Count requests in current window
        request_count = len(self.requests[key])

        if request_count >= config.max_requests:
            # Calculate retry after time
            oldest_timestamp = self.requests[key][0]
            retry_after = int(oldest_timestamp +
                              config.window_seconds - current_time)
            return True, max(0, retry_after)

        # Add new request
        self.requests[key].append(current_time)
        return False, None

    def check_download_limit(self, key: str, tier: UserTier = UserTier.FREE) -> Tuple[bool, Optional[int]]:
        """
        Check if downloads should be limited.
        Returns (is_limited, retry_after_seconds)
        """
        config = self.tier_configs[tier]
        current_time = time.time()

        # Clean old downloads
        self._clean_old_downloads(key, config.window_seconds)

        # Initialize download list if not exists
        if key not in self.downloads:
            self.downloads[key] = []

        # Count downloads in current window
        download_count = len(self.downloads[key])

        if download_count >= config.download_limit:
            # Calculate retry after time
            oldest_timestamp = self.downloads[key][0]
            retry_after = int(oldest_timestamp +
                              config.window_seconds - current_time)
            return True, max(0, retry_after)

        # Add new download
        self.downloads[key].append(current_time)
        return False, None

    def check_bulk_download_limit(self, key: str, tier: UserTier = UserTier.FREE) -> Tuple[bool, Optional[int]]:
        """
        Check if bulk downloads should be limited.
        Returns (is_limited, retry_after_seconds)
        """
        config = self.tier_configs[tier]
        current_time = time.time()

        # Clean old bulk downloads
        self._clean_old_bulk_downloads(key, config.window_seconds)

        # Initialize bulk download list if not exists
        if key not in self.bulk_downloads:
            self.bulk_downloads[key] = []

        # Count bulk downloads in current window
        bulk_count = len(self.bulk_downloads[key])

        if bulk_count >= config.bulk_download_limit:
            # Calculate retry after time
            oldest_timestamp = self.bulk_downloads[key][0]
            retry_after = int(oldest_timestamp +
                              config.window_seconds - current_time)
            return True, max(0, retry_after)

        # Add new bulk download
        self.bulk_downloads[key].append(current_time)
        return False, None

    def get_remaining_quota(self, key: str, tier: UserTier = UserTier.FREE) -> Dict[str, int]:
        """Get remaining quota for requests and bulk downloads."""
        config = self.tier_configs[tier]

        # Clean old data
        self._clean_old_requests(key, config.window_seconds)
        self._clean_old_bulk_downloads(key, config.window_seconds)
        self._clean_old_downloads(key, config.window_seconds)

        # Calculate remaining quotas
        requests_used = len(self.requests.get(key, []))
        bulk_downloads_used = len(self.bulk_downloads.get(key, []))
        downloads_used = len(self.downloads.get(key, []))

        return {
            "remaining_requests": config.max_requests - requests_used,
            "remaining_bulk_downloads": config.bulk_download_limit - bulk_downloads_used,
            "remaining_downloads": config.download_limit - downloads_used,
            "tier": tier
        }
