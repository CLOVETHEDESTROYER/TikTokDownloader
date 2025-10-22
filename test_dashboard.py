#!/usr/bin/env python3
"""
Test script for the Dashboard API endpoints
"""

import httpx
import asyncio
import os
import sys

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

async def test_dashboard_stats():
    """Test dashboard stats endpoint."""
    print("\n📊 Testing Dashboard Stats")
    print("==========================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/social/dashboard/stats",
                headers={"X-API-Key": API_KEY}
            )
            response.raise_for_status()
            stats = response.json()
            print(f"✅ Dashboard stats retrieved successfully")
            print(f"   Total Accounts: {stats.get('total_accounts', 0)}")
            print(f"   Active Accounts: {stats.get('active_accounts', 0)}")
            print(f"   Content Collected: {stats.get('total_content_collected', 0)}")
            print(f"   Scheduled Posts: {stats.get('scheduled_posts', 0)}")
            return stats
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to get dashboard stats: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

async def test_social_accounts():
    """Test social accounts endpoint."""
    print("\n👥 Testing Social Accounts")
    print("==========================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/social/accounts",
                headers={"X-API-Key": API_KEY}
            )
            response.raise_for_status()
            accounts = response.json()
            print(f"✅ Successfully retrieved {len(accounts)} social accounts")
            for account in accounts:
                print(f"   - {account.get('username')} ({account.get('platform')}, ID: {account.get('id')})")
            return accounts
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to get social accounts: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return []

async def test_content_items():
    """Test content items endpoint."""
    print("\n📦 Testing Content Items")
    print("========================")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/social/content?limit=10",
                headers={"X-API-Key": API_KEY}
            )
            response.raise_for_status()
            content = response.json()
            print(f"✅ Successfully retrieved {len(content)} content items")
            for item in content[:3]:  # Show first 3
                print(f"   - {item.get('id')} ({item.get('platform')}, {item.get('content_type')})")
            return content
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to get content items: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return []

async def test_publishing_platforms():
    """Test publishing platforms endpoint."""
    print("\n📱 Testing Publishing Platforms")
    print("===============================")
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
            return platforms
    except httpx.HTTPStatusError as e:
        print(f"❌ Failed to get publishing platforms: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    return None

async def main():
    """Run all dashboard tests."""
    print("🎬 Dashboard API Test Suite")
    print("=" * 30)
    
    # Test API health first
    await test_api_health()
    
    # Test dashboard endpoints
    await test_dashboard_stats()
    await test_social_accounts()
    await test_content_items()
    await test_publishing_platforms()
    
    print("\n🎯 Dashboard Test Suite Completed!")
    print("\n📝 Next Steps:")
    print("   1. Open http://localhost:3000/dashboard in your browser")
    print("   2. The dashboard should now work without errors")
    print("   3. Connect your Instagram account to start using the system")

if __name__ == "__main__":
    asyncio.run(main())
