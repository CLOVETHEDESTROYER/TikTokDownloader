from fastapi import Request, HTTPException, Depends
from typing import Tuple
from ..services.rate_limiter import RateLimiter, UserTier

rate_limiter = RateLimiter()


async def get_user_ip_and_tier(request: Request) -> Tuple[str, UserTier]:
    """
    Get the user's IP address and tier.
    In a real application, you would also check for authentication
    and get the user's actual tier from a database.
    """
    # Get the client's IP address
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0]
    else:
        ip = request.client.host

    # For now, everyone is on the free tier
    # In a real application, you would check the user's subscription status
    return ip, UserTier.FREE


async def check_rate_limit(
    request: Request,
    ip_and_tier: Tuple[str, UserTier] = Depends(get_user_ip_and_tier)
) -> None:
    """Check if the request should be rate limited."""
    ip, tier = ip_and_tier
    is_limited, retry_after = rate_limiter.is_rate_limited(ip, tier)

    if is_limited:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Too many requests",
                "retry_after_seconds": retry_after
            }
        )


async def check_download_limit(
    request: Request,
    ip_and_tier: Tuple[str, UserTier] = Depends(get_user_ip_and_tier)
) -> None:
    """Check if the user has exceeded their download limit."""
    ip, tier = ip_and_tier
    is_limited, retry_after = rate_limiter.check_download_limit(ip, tier)

    if is_limited:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Download limit reached. Upgrade to Premium for more downloads.",
                "retry_after_seconds": retry_after
            }
        )


async def check_bulk_download_limit(
    request: Request,
    ip_and_tier: Tuple[str, UserTier] = Depends(get_user_ip_and_tier)
) -> None:
    """Check if bulk downloads should be limited."""
    ip, tier = ip_and_tier
    is_limited, retry_after = rate_limiter.check_bulk_download_limit(ip, tier)

    if is_limited:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Bulk download limit reached",
                "retry_after_seconds": retry_after
            }
        )


async def get_quota(
    request: Request,
    ip_and_tier: Tuple[str, UserTier] = Depends(get_user_ip_and_tier)
) -> dict:
    """Get the user's remaining quota."""
    ip, tier = ip_and_tier
    return rate_limiter.get_remaining_quota(ip, tier)
