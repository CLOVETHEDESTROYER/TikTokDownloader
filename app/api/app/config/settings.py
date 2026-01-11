import os
from typing import Optional
from functools import lru_cache
from ..core.config import settings

@lru_cache()
def get_settings():
    """Get application settings with caching"""
    return settings

# Define constants used across the application
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "downloads")
LOG_FOLDER = os.getenv("LOG_FOLDER", "logs")
DEFAULT_VIDEO_QUALITY = "medium" 