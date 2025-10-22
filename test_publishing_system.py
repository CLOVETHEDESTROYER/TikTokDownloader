#!/usr/bin/env python3
"""
Test script for the TikTok/Instagram Publishing System
"""

import httpx
import asyncio
import os
import sys
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "website_key_123"  # Your app's API key from .env file

async def test_api_health():
    """Test if the API is running."""
    print("\n🏥 Testing API Health")
    print("==============================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL.replace('/api/v1', '')}/health", timeout=10)
            response.raise_for_status()
            health_status = response.json()
            print(f"✅ API is healthy")
            print(f"📊 Status: {health_status.get('status')}")
            print(f"🔧 Environment: {health_status.get('env')}")
    except httpx.RequestError as e:
        print(f"❌ Cannot connect to API: {e}")
        print("   Please start the server first: cd app/api && source venv/bin/activate && python -m uvicorn app.main:app --reload")
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(f"❌ API Health check failed: {e}")
        sys.exit(1)

async def test_get_supported_platforms():
    """Test getting supported publishing platforms."""
    print("\n📱 Testing Supported Platforms")
    print("=================================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/publishing/platforms",
                headers={"X-API-Key": API_KEY}
            )
            response.raise_for_status()
            platforms = response.json()
            print(f"✅ Successfully retrieved supported platforms")
            for platform in platforms.get('supported_platforms', []):
                print(f"   - {platform['name']} ({platform['platform']})")
                print(f"     Features: {', '.join(platform['features'])}")
                print(f"     Max Duration: {platform['max_video_duration']}s")
                print(f"     Max Size: {platform['max_file_size']}MB")
            return platforms
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to get supported platforms: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

async def test_schedule_post():
    """Test scheduling a post for future publishing."""
    print("\n📅 Testing Schedule Post")
    print("=========================")
    try:
        # Schedule a post for 1 hour from now
        scheduled_time = datetime.now() + timedelta(hours=1)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/publishing/schedule",
                headers={"X-API-Key": API_KEY},
                params={
                    "content_id": "test_content_123",
                    "target_platforms": ["tiktok", "instagram"],
                    "scheduled_time": scheduled_time.isoformat(),
                    "caption": "Test scheduled post! 🚀 #test #automation",
                    "hashtags": ["test", "automation", "socialmedia"],
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "location_id": None
                }
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ Successfully scheduled post")
            print(f"   Scheduled Post ID: {result.get('scheduled_post_id')}")
            print(f"   Content ID: {result.get('content_id')}")
            print(f"   Target Platforms: {result.get('target_platforms')}")
            print(f"   Scheduled Time: {result.get('scheduled_time')}")
            return result
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to schedule post: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

async def test_publish_now():
    """Test immediate publishing (mock)."""
    print("\n🚀 Testing Publish Now (Mock)")
    print("==============================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/publishing/publish-now",
                headers={"X-API-Key": API_KEY},
                params={
                    "content_id": "test_content_456",
                    "target_platforms": ["tiktok", "instagram"],
                    "caption": "Test immediate post! ⚡ #test #immediate",
                    "hashtags": ["test", "immediate", "socialmedia"],
                    "privacy_level": "PUBLIC_TO_EVERYONE",
                    "location_id": None
                }
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ Publish now request processed")
            print(f"   Success: {result.get('success')}")
            print(f"   Content ID: {result.get('content_id')}")
            print(f"   Published At: {result.get('published_at')}")
            
            if 'platforms' in result:
                for platform, platform_result in result['platforms'].items():
                    print(f"   {platform.upper()}: {'✅ Success' if platform_result.get('success') else '❌ Failed'}")
                    if not platform_result.get('success'):
                        print(f"     Error: {platform_result.get('error')}")
            
            return result
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to publish now: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

async def test_list_scheduled_posts():
    """Test listing scheduled posts."""
    print("\n📋 Testing List Scheduled Posts")
    print("=================================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/publishing/scheduled-posts",
                headers={"X-API-Key": API_KEY}
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ Successfully retrieved scheduled posts")
            print(f"   Total Count: {result.get('total_count', 0)}")
            print(f"   Filters: {result.get('filters', {})}")
            
            scheduled_posts = result.get('scheduled_posts', [])
            for post in scheduled_posts[:3]:  # Show first 3
                print(f"   - Post ID: {post.get('id', 'N/A')}")
                print(f"     Platforms: {post.get('target_platforms', [])}")
                print(f"     Scheduled: {post.get('scheduled_time', 'N/A')}")
            
            return result
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to list scheduled posts: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

async def test_get_publish_status():
    """Test getting publish status for content."""
    print("\n📊 Testing Get Publish Status")
    print("==============================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/publishing/status/test_content_123",
                headers={"X-API-Key": API_KEY}
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ Successfully retrieved publish status")
            print(f"   Content ID: {result.get('content_id')}")
            print(f"   Status: {result.get('status')}")
            print(f"   Published Platforms: {result.get('published_platforms', [])}")
            print(f"   Last Updated: {result.get('last_updated')}")
            return result
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to get publish status: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

async def test_cleanup_after_publish():
    """Test cleanup after publishing."""
    print("\n🧹 Testing Cleanup After Publish")
    print("==================================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE_URL}/publishing/cleanup/test_content_123",
                headers={"X-API-Key": API_KEY}
            )
            response.raise_for_status()
            result = response.json()
            print(f"✅ Cleanup request processed")
            print(f"   Success: {result.get('success')}")
            print(f"   Content ID: {result.get('content_id')}")
            print(f"   Message: {result.get('message')}")
            return result
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to cleanup: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

async def main():
    """Run all publishing system tests."""
    print("🎬 TikTok/Instagram Publishing System Test Suite")
    print("=" * 50)
    
    # Test API health first
    await test_api_health()
    
    # Test publishing system features
    await test_get_supported_platforms()
    await test_schedule_post()
    await test_publish_now()
    await test_list_scheduled_posts()
    await test_get_publish_status()
    await test_cleanup_after_publish()
    
    print("\n🎯 Publishing System Test Suite Completed!")
    print("\n📝 Next Steps:")
    print("   1. Set up real TikTok and Instagram API credentials")
    print("   2. Test with actual video files")
    print("   3. Implement database persistence for scheduled posts")
    print("   4. Add error handling and retry mechanisms")
    print("   5. Integrate with the web dashboard")

if __name__ == "__main__":
    asyncio.run(main())
