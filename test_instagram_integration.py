#!/usr/bin/env python3
"""
Test script for Instagram integration functionality
"""

import requests
import json
import time
import sys

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
API_KEY = "website_key_123"  # Your app's API key from .env file

def test_dashboard_stats():
    """Test dashboard stats endpoint"""
    print("📊 Testing Dashboard Stats")
    print("=" * 40)
    
    headers = {
        "X-API-Key": API_KEY
    }
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/social/dashboard/stats",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Dashboard stats retrieved successfully")
            print(f"📈 Total accounts: {stats.get('total_accounts', 0)}")
            print(f"📈 Active accounts: {stats.get('active_accounts', 0)}")
            print(f"📈 Content collected: {stats.get('total_content_collected', 0)}")
            print(f"📈 Downloads pending: {stats.get('downloads_pending', 0)}")
            print(f"📈 Scheduled posts: {stats.get('scheduled_posts', 0)}")
        else:
            print(f"❌ Failed to get dashboard stats: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Error getting dashboard stats: {e}")

def test_instagram_auth_url():
    """Test Instagram OAuth URL generation"""
    print("\n🔐 Testing Instagram OAuth URL")
    print("=" * 40)
    
    headers = {
        "X-API-Key": API_KEY
    }
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/social/instagram/auth-url",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            auth_url = data.get('auth_url')
            print(f"✅ Instagram OAuth URL generated successfully")
            print(f"🔗 Auth URL: {auth_url}")
            print(f"📝 Copy this URL to test Instagram connection in browser")
        else:
            print(f"❌ Failed to get Instagram auth URL: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Error getting Instagram auth URL: {e}")

def test_social_accounts():
    """Test social accounts endpoint"""
    print("\n👥 Testing Social Accounts")
    print("=" * 40)
    
    headers = {
        "X-API-Key": API_KEY
    }
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/social/accounts",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            accounts = response.json()
            print(f"✅ Retrieved {len(accounts)} social accounts")
            
            for account in accounts:
                print(f"📱 Platform: {account.get('platform', 'Unknown')}")
                print(f"👤 Username: {account.get('username', 'Unknown')}")
                print(f"🟢 Active: {account.get('is_active', False)}")
                print(f"🆔 ID: {account.get('account_id', 'Unknown')}")
                print("-" * 20)
        else:
            print(f"❌ Failed to get social accounts: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Error getting social accounts: {e}")

def test_collected_content():
    """Test collected content endpoint"""
    print("\n📱 Testing Collected Content")
    print("=" * 40)
    
    headers = {
        "X-API-Key": API_KEY
    }
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/social/content?limit=10",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            content = response.json()
            print(f"✅ Retrieved {len(content)} content items")
            
            for item in content:
                print(f"📱 Platform: {item.get('platform', 'Unknown')}")
                print(f"🎬 Type: {item.get('content_type', 'Unknown')}")
                print(f"📝 Title: {item.get('title', 'No title')[:50]}...")
                print(f"📊 Status: {item.get('status', 'Unknown')}")
                print(f"🔗 URL: {item.get('original_url', 'No URL')}")
                print("-" * 20)
        else:
            print(f"❌ Failed to get collected content: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Error getting collected content: {e}")

def test_instagram_content_collection():
    """Test Instagram content collection (mock)"""
    print("\n📥 Testing Instagram Content Collection")
    print("=" * 40)
    
    headers = {
        "X-API-Key": API_KEY
    }
    
    # Test collecting saved posts
    try:
        response = requests.post(
            f"{API_BASE_URL}/social/instagram/collect-saved",
            params={"account_id": "mock_account_123", "limit": 5},
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Content collection successful")
            print(f"📈 New content collected: {result.get('collected_count', 0)}")
            print(f"📱 New items: {len(result.get('new_content', []))}")
            print(f"🔄 Existing items: {len(result.get('existing_content', []))}")
            
            if result.get('errors'):
                print(f"⚠️ Errors: {result['errors']}")
        else:
            print(f"❌ Failed to collect content: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Error collecting Instagram content: {e}")

def test_api_health():
    """Test if the API is running and accessible"""
    print("🏥 Testing API Health")
    print("=" * 30)
    
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api/v1', '')}/health", timeout=10)
        
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
    print("🚀 Instagram Integration Test Suite")
    print("=" * 60)
    
    # Check if API is running
    if not test_api_health():
        print("\n❌ API is not accessible. Please start the server first:")
        print("   cd app/api && source venv/bin/activate && python -m uvicorn app.main:app --reload")
        sys.exit(1)
    
    # Run tests
    test_dashboard_stats()
    test_instagram_auth_url()
    test_social_accounts()
    test_collected_content()
    test_instagram_content_collection()
    
    print("\n🎯 Instagram Integration Test completed!")
    print("\n📝 Next Steps:")
    print("1. Set up Instagram App in Meta Developer Console")
    print("2. Add your Instagram App ID and Secret to .env file")
    print("3. Test the OAuth flow with a real Instagram account")
    print("4. Access the web dashboard at http://localhost:3000/dashboard")
