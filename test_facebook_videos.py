#!/usr/bin/env python3
"""
Test script for Facebook video download functionality
"""

import requests
import json
import time
import sys
import os

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "website_key_123"  # Your app's API key from .env file


def test_facebook_video_download():
    """Test downloading a Facebook video"""

    # Example Facebook video URL (replace with a real one)
    video_url = "https://www.facebook.com/watch/example_video_id"

    print("📘 Testing Facebook Video Download")
    print("=" * 50)

    # Test 1: Basic download request
    print(f"📥 Testing download for: {video_url}")

    download_data = {
        "url": video_url,
        "platform": "facebook",
        "quality": "high"
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    try:
        # Create download request
        response = requests.post(
            f"{API_BASE_URL}/download",
            json=download_data,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            session_id = result.get("session_id")
            print(f"✅ Download request created successfully")
            print(f"📋 Session ID: {session_id}")
            print(f"📊 Status: {result.get('status')}")

            # Test 2: Check download status
            print(f"\n⏳ Checking download status...")

            for i in range(10):  # Check up to 10 times
                status_response = requests.get(
                    f"{API_BASE_URL}/status/{session_id}",
                    headers=headers,
                    timeout=10
                )

                if status_response.status_code == 200:
                    status = status_response.json()
                    print(
                        f"📈 Progress: {status.get('progress', 0)}% - Status: {status.get('status')}")

                    if status.get('status') == 'completed':
                        print(f"🎉 Download completed successfully!")
                        print(f"📁 File: {status.get('filename', 'Unknown')}")
                        break
                    elif status.get('status') == 'failed':
                        print(
                            f"❌ Download failed: {status.get('error', 'Unknown error')}")
                        break
                else:
                    print(
                        f"⚠️  Status check failed: {status_response.status_code}")

                time.sleep(2)  # Wait 2 seconds between checks
            else:
                print("⏰ Download timeout - check manually")

        else:
            print(f"❌ Download request failed: {response.status_code}")
            print(f"📝 Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"🌐 Network error: {e}")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")


def test_facebook_advanced_download():
    """Test advanced Facebook download with metadata"""

    print("\n🔬 Testing Advanced Facebook Download")
    print("=" * 50)

    # Example Facebook Reel URL
    reel_url = "https://www.facebook.com/reel/example_reel_id"

    download_data = {
        "url": reel_url,
        "quality": "high",
        "include_metadata": True,
        "include_captions": False
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/facebook/download-advanced",
            json=download_data,
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Advanced download successful")
            print(f"📋 Session ID: {result.get('session_id')}")
            print(f"🎬 Content Type: {result.get('content_type')}")
            print(f"📺 Is Live: {result.get('is_live')}")
            print(
                f"📊 Metadata: {json.dumps(result.get('metadata', {}), indent=2)}")
        else:
            print(f"❌ Advanced download failed: {response.status_code}")
            print(f"📝 Response: {response.text}")

    except Exception as e:
        print(f"💥 Error in advanced download: {e}")


def test_api_health():
    """Test if the API is running and accessible"""

    print("🏥 Testing API Health")
    print("=" * 30)

    try:
        response = requests.get(
            f"{API_BASE_URL.replace('/api/v1', '')}/health", timeout=10)

        if response.status_code == 200:
            health = response.json()
            print(f"✅ API is healthy")
            print(f"📊 Status: {health.get('status')}")
            print(f"🔧 Environment: {health.get('env')}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"🌐 Cannot connect to API: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Facebook Video Download Test Suite")
    print("=" * 60)

    # Check if API is running
    if not test_api_health():
        print("\n❌ API is not accessible. Please start the server first:")
        print("   cd app/api && uvicorn app.main:app --reload")
        sys.exit(1)

    # Run tests
    test_facebook_video_download()
    test_facebook_advanced_download()

    print("\n🎯 Test completed!")
    print("\n📝 Note: Replace the example URLs with real Facebook video URLs to test")
    print("🔑 Make sure to set the correct API_KEY in this script")
