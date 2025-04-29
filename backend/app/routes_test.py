from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import os
import time
from .models.download import DownloadStatus, Platform
from .services.download_manager import DownloadManager

router = APIRouter()
download_manager = DownloadManager()


@router.get("/create-test-session")
async def create_test_session():
    """Create a test download session for debugging."""
    try:
        # Ensure the downloads directory exists
        os.makedirs("downloads", exist_ok=True)

        # Create a test video file (if it doesn't exist)
        test_filename = "test_video.mp4"
        file_path = os.path.join("downloads", test_filename)
        if not os.path.exists(file_path):
            # Create an empty file
            with open(file_path, "wb") as f:
                # Write a small amount of data so it's not completely empty
                f.write(b"TEST VIDEO FILE")

        # Create a download session
        test_url = "https://www.example.com/test-video"
        session_id = await download_manager.create_download(url=test_url, platform=Platform.TIKTOK)

        # Update the session to completed status
        download_manager.active_downloads[session_id].update({
            "status": DownloadStatus.COMPLETED,
            "filename": test_filename,
            "created_at": time.time(),
            "expires_at": time.time() + 300  # Expires in 5 minutes
        })

        # Get the status
        status = await download_manager.get_download_status(session_id)

        return {
            "message": "Test download session created",
            "session_id": session_id,
            "status": str(status.status),
            "filename": status.filename,
            "expires_at": status.expires_at,
            "url": status.url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
