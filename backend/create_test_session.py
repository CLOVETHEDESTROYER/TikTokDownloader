"""
Quick script to create a test download session in the database.
This will create a completed download record that points to a test video file.
"""

import asyncio
import os
import time
import uuid
from app.models.download import DownloadStatus, Platform
from app.services.download_manager import DownloadManager


async def create_test_session():
    # Create download manager
    download_manager = DownloadManager()

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

    # Print the session details
    status = await download_manager.get_download_status(session_id)
    print("\n=== TEST DOWNLOAD SESSION CREATED ===")
    print(f"Session ID: {session_id}")
    print(f"Status: {status.status}")
    print(f"Filename: {status.filename}")
    print(f"Expires at: {status.expires_at}")
    print(f"URL: {status.url}")
    print("======================================\n")

    return session_id

if __name__ == "__main__":
    # Run the async function
    session_id = asyncio.run(create_test_session())
    print(f"Use this session ID for testing: {session_id}")
