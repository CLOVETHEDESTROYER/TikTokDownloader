#!/usr/bin/env python3
"""
Example script showing how to use the YouTube Shorts download functionality
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "dev_website_key_123"  # Your app's API key from .env file


def download_youtube_shorts(shorts_url: str, quality: str = "high"):
    """
    Download a YouTube Shorts video

    Args:
        shorts_url: YouTube Shorts URL (e.g., https://www.youtube.com/shorts/VIDEO_ID)
        quality: Video quality ('high', 'medium', 'low')
    """

    print(f"🎬 Downloading YouTube Shorts: {shorts_url}")

    # Prepare the request
    download_data = {
        "url": shorts_url,
        "platform": "youtube",
        "quality": quality
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    try:
        # Step 1: Create download request
        print("📥 Creating download request...")
        response = requests.post(
            f"{API_BASE_URL}/download",
            json=download_data,
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ Failed to create download: {response.status_code}")
            print(f"Response: {response.text}")
            return None

        result = response.json()
        session_id = result.get("session_id")
        print(f"✅ Download request created (Session: {session_id})")

        # Step 2: Monitor download progress
        print("⏳ Monitoring download progress...")

        while True:
            status_response = requests.get(
                f"{API_BASE_URL}/status/{session_id}",
                headers=headers,
                timeout=10
            )

            if status_response.status_code != 200:
                print(f"❌ Failed to get status: {status_response.status_code}")
                break

            status = status_response.json()
            progress = status.get('progress', 0)
            status_text = status.get('status', 'unknown')

            print(f"📊 Progress: {progress}% - Status: {status_text}")

            if status_text == 'completed':
                print("🎉 Download completed successfully!")
                print(f"📁 Filename: {status.get('filename', 'Unknown')}")
                return session_id
            elif status_text == 'failed':
                print(
                    f"❌ Download failed: {status.get('error', 'Unknown error')}")
                return None

            time.sleep(2)  # Wait 2 seconds before next check

    except requests.exceptions.RequestException as e:
        print(f"🌐 Network error: {e}")
        return None
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return None


def download_with_advanced_options(shorts_url: str):
    """
    Download YouTube Shorts with advanced options and metadata
    """

    print(f"🔬 Downloading with advanced options: {shorts_url}")

    download_data = {
        "url": shorts_url,
        "quality": "high",
        "include_metadata": True,
        "include_subtitles": False
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/youtube/download-advanced",
            json=download_data,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Advanced download successful!")
            print(f"📋 Session ID: {result.get('session_id')}")
            print(f"🎬 Content Type: {result.get('content_type')}")
            print(f"📺 Is Shorts: {result.get('is_shorts')}")

            # Display metadata
            metadata = result.get('metadata', {})
            if metadata:
                print("\n📊 Video Metadata:")
                print(f"  Title: {metadata.get('title', 'N/A')}")
                print(f"  Author: {metadata.get('author', 'N/A')}")
                print(f"  Duration: {metadata.get('duration', 0)} seconds")
                print(f"  Views: {metadata.get('view_count', 0):,}")
                print(f"  Likes: {metadata.get('like_count', 0):,}")
                print(f"  Upload Date: {metadata.get('upload_date', 'N/A')}")
                print(f"  Thumbnail: {metadata.get('thumbnail_url', 'N/A')}")

            return result.get('session_id')
        else:
            print(f"❌ Advanced download failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"💥 Error in advanced download: {e}")
        return None


def batch_download_shorts(urls: list, quality: str = "high"):
    """
    Download multiple YouTube Shorts videos
    """

    print(f"📦 Batch downloading {len(urls)} videos...")

    download_data = {
        "urls": urls,
        "platform": "youtube",
        "quality": quality
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/batch-download",
            json=download_data,
            headers=headers,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            session_id = result.get('session_id')
            total_urls = result.get('total_urls', 0)

            print(f"✅ Batch download started (Session: {session_id})")
            print(f"📊 Total URLs: {total_urls}")

            # Monitor batch progress
            while True:
                status_response = requests.get(
                    f"{API_BASE_URL}/status/{session_id}",
                    headers=headers,
                    timeout=10
                )

                if status_response.status_code == 200:
                    status = status_response.json()
                    progress = status.get('progress', 0)
                    status_text = status.get('status', 'unknown')

                    print(
                        f"📊 Batch Progress: {progress}% - Status: {status_text}")

                    if status_text in ['completed', 'failed']:
                        break

                time.sleep(3)

            return session_id
        else:
            print(f"❌ Batch download failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"💥 Error in batch download: {e}")
        return None


if __name__ == "__main__":
    print("🚀 YouTube Shorts Download Examples")
    print("=" * 50)

    # Example 1: Basic download
    print("\n1️⃣ Basic YouTube Shorts Download")
    shorts_url = "https://www.youtube.com/shorts/example_video_id"
    session_id = download_youtube_shorts(shorts_url, "high")

    # Example 2: Advanced download with metadata
    print("\n2️⃣ Advanced Download with Metadata")
    session_id = download_with_advanced_options(shorts_url)

    # Example 3: Batch download
    print("\n3️⃣ Batch Download")
    urls = [
        "https://www.youtube.com/shorts/video1",
        "https://www.youtube.com/shorts/video2",
        "https://www.youtube.com/watch?v=regular_video"
    ]
    session_id = batch_download_shorts(urls, "medium")

    print("\n🎯 Examples completed!")
    print("\n📝 Note: Replace example URLs with real YouTube/Shorts URLs")
    print("🔑 Make sure to set the correct API_KEY")
