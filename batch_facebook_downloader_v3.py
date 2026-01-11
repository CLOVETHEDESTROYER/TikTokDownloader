#!/usr/bin/env python3
"""
Batch Facebook Video Downloader v3
Uses original share URLs directly - yt-dlp should handle them
"""

import requests
import json
import time
import sys
import os
import re
from typing import List

# Configuration
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
API_ENDPOINT = f"{API_BASE_URL}/api/v1/facebook/batch"
API_KEY = os.getenv("API_KEY", "website_key_123")

# Facebook URLs to download - using original share URLs
FACEBOOK_URLS = [
    "https://www.facebook.com/share/r/1aHKgeNaZ5/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1CXhmsrQRE/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1Aa6LZtR2T/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1BR2VoMGNb/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/14RLzaAsB3Y/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1BsWQWvgwZ/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/17CoMGx6aV/?mibextid=wwXIfr",
    "https://www.facebook.com/share/v/1AEE17uAee/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1akUYXy1Nb/?mibextid=wwXIfr",
    "https://www.facebook.com/share/v/1BnS3BoZ5N/?mibextid=wwXIfr",
    "https://www.facebook.com/share/v/1aEv9yT8XV/?mibextid=wwXIfr",
    "https://www.facebook.com/share/v/1QKRrwq7FY/?mibextid=wwXIfr",
    "https://www.facebook.com/share/v/17byddrG14/?mibextid=wwXIfr",
    "https://www.facebook.com/share/v/17TUhUbjs4/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/16ncGKCJqL/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1Ay99Lt9HK/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1DB8afDjAd/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/17ieRvj5fJ/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/17XS7t8QGj/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1Ece9Rwz7W/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1D3jk4DFzn/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1MxEVxSqrc/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/17D4FN3pLN/?mibextid=wwXIfr",
    "https://www.facebook.com/share/r/1VhtNrGk8v/?mibextid=wwXIfr",
]


def check_api_health() -> bool:
    """Check if the API is running and accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def download_facebook_batch(urls: List[str], quality: str = "high") -> List[dict]:
    """Download multiple Facebook videos using the batch endpoint"""
    
    print(f"\n📥 Starting batch download of {len(urls)} Facebook videos...")
    print(f"🔗 API Endpoint: {API_ENDPOINT}")
    print(f"⚙️  Quality: {quality}")
    print(f"📋 Using original share URLs (yt-dlp should handle them)\n")
    
    # Prepare request data
    request_data = {
        "urls": urls,
        "platform": "facebook",
        "quality": quality
    }
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
    }
    
    # Add API key if provided
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    
    try:
        print("⏳ Sending batch download request...")
        print("   (This may take several minutes for 24 videos)\n")
        start_time = time.time()
        
        response = requests.post(
            API_ENDPOINT,
            json=request_data,
            headers=headers,
            timeout=900  # 15 minute timeout for batch operations
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Batch download completed in {elapsed_time:.2f} seconds ({elapsed_time/60:.1f} minutes)\n")
            print(f"📊 Received {len(results)} results from API\n")
            return results
        else:
            print(f"❌ Batch download failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            try:
                error_data = response.json()
                print(f"📋 Error details: {json.dumps(error_data, indent=2)}")
            except:
                pass
            return []
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out. The batch operation may still be processing.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []


def print_results(results: List[dict], original_urls: List[str]):
    """Print download results in a formatted way"""
    if not results:
        print("⚠️  No results to display")
        return
    
    print("=" * 80)
    print("📊 DOWNLOAD RESULTS")
    print("=" * 80)
    
    successful = 0
    failed = 0
    
    for i, result in enumerate(results, 1):
        status = result.get("status", "unknown")
        # Use original URL for display
        url = original_urls[i-1] if i <= len(original_urls) else result.get("url", "N/A")
        download_url = result.get("download_url", "")
        content_type = result.get("content_type", "unknown")
        session_id = result.get("session_id", "N/A")
        title = result.get("title", "")
        
        # Truncate URL for display
        url_display = url[:70] + "..." if len(url) > 70 else url
        print(f"\n[{i}/{len(results)}] {url_display}")
        print(f"   Status: {status}")
        
        if status == "completed" and download_url:
            print(f"   ✅ Download URL: {API_BASE_URL}{download_url}")
            if title:
                print(f"   📹 Title: {title[:60]}")
            print(f"   🎬 Content Type: {content_type}")
            print(f"   🆔 Session ID: {session_id}")
            successful += 1
        elif status == "failed":
            error = result.get("error", result.get("message", "Unknown error"))
            # Clean up ANSI color codes from error messages
            error = re.sub(r'\x1b\[[0-9;]*m', '', error)
            print(f"   ❌ Error: {error[:200]}")
            failed += 1
        else:
            print(f"   ⚠️  Status: {status}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"📈 SUMMARY: {successful} successful, {failed} failed out of {len(results)} total")
    if successful > 0:
        print(f"🎉 Successfully downloaded {successful} video(s)!")
    if failed > 0:
        print(f"⚠️  {failed} video(s) failed to download")
    print("=" * 80)


def main():
    """Main function"""
    print("🚀 Facebook Batch Video Downloader v3")
    print("=" * 80)
    print("📋 Using original Facebook share URLs")
    print("   yt-dlp should handle share URLs directly")
    print("=" * 80)
    
    # Check API health
    print(f"\n🔍 Checking API health at {API_BASE_URL}...")
    if not check_api_health():
        print(f"\n❌ API is not accessible at {API_BASE_URL}")
        print("\n💡 Please make sure the backend is running:")
        print("   cd app/api && ./start_api.sh")
        print("   OR")
        print("   cd app/api && uvicorn app.main:app --reload")
        sys.exit(1)
    
    print("✅ API is running and accessible\n")
    
    # Download all videos using original share URLs
    results = download_facebook_batch(FACEBOOK_URLS, quality="high")
    
    # Print results
    if results:
        print_results(results, FACEBOOK_URLS)
    else:
        print("\n⚠️  No results returned from the API")
    
    print("\n🎯 Batch download process completed!")


if __name__ == "__main__":
    main()

