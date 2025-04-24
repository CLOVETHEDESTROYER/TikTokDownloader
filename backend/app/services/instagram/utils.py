import os
import re
from typing import Dict, Optional
from ...core.config import settings
from ...core.exceptions import InvalidURLError


def load_cookies(cookie_file: str = None) -> Dict[str, str]:
    """Load Instagram cookies from file."""
    if not cookie_file:
        cookie_file = os.path.join(
            settings.CONFIG_DIR, 'instagram_cookies.txt')

    if not os.path.exists(cookie_file):
        return {}

    cookies = {}
    try:
        with open(cookie_file, 'r') as f:
            for line in f:
                if not line.startswith('#') and line.strip():
                    fields = line.strip().split('\t')
                    if len(fields) >= 7:
                        cookies[fields[5]] = fields[6]
    except Exception as e:
        print(f"Error loading cookies: {e}")
    return cookies


def validate_instagram_url(url: str) -> bool:
    """Validate if the URL is a valid Instagram URL."""
    patterns = [
        r'https?://(?:www\.)?instagram\.com/p/[\w-]+/?',  # Posts
        r'https?://(?:www\.)?instagram\.com/reel/[\w-]+/?',  # Reels
        r'https?://(?:www\.)?instagram\.com/stories/[\w-]+/[\d]+/?',  # Stories
    ]

    return any(re.match(pattern, url) for pattern in patterns)


def get_media_type(url: str) -> Optional[str]:
    """Determine the type of Instagram media from the URL."""
    if '/p/' in url:
        return 'post'
    elif '/reel/' in url:
        return 'reel'
    elif '/stories/' in url:
        return 'story'
    return None


def clean_filename(filename: str) -> str:
    """Clean filename to be safe for saving."""
    return re.sub(r'[^\w\-_\. ]', '_', filename)
