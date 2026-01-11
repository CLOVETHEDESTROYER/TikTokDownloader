#!/usr/bin/env python3
"""
Batch Facebook Video Downloader v2
Resolves Facebook share URLs to direct video URLs, then downloads them
"""

import requests
import json
import time
import sys
import os
import re
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

# Configuration
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
API_ENDPOINT = f"{API_BASE_URL}/api/v1/facebook/batch"
API_KEY = os.getenv("API_KEY", "website_key_123")

# Facebook URLs to download
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


def resolve_facebook_url(share_url: str) -> Optional[str]:
    """
    Resolve Facebook share URL to direct video URL
    Facebook share URLs have format: /share/r/{video_id} or /share/v/{video_id}
    We'll try to convert them to watch URLs
    """
    try:
        # Extract video ID from share URL
        # Pattern: /share/r/{id} or /share/v/{id}
        match = re.search(r'/share/[rv]/([^/?]+)', share_url)
        if match:
            video_id = match.group(1)
            # Try to construct a watch URL
            # Facebook watch URLs can be: https://www.facebook.com/watch/?v={video_id}
            watch_url = f"https://www.facebook.com/watch/?v={video_id}"
            return watch_url
        
        # If already a watch URL or other format, return as-is
        return share_url
    except Exception as e:
        print(f"⚠️  Error resolving URL {share_url}: {e}")
        return share_url


def resolve_urls_with_redirect(share_url: str) -> Optional[str]:
    """
    Try to resolve URL by following redirects
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        # Follow redirects but don't download
        response = requests.head(share_url, headers=headers, allow_redirects=True, timeout=10)
        final_url = response.url
        
        # If we got redirected to a different URL, use that
        if final_url != share_url and 'facebook.com' in final_url:
            return final_url
        
        return share_url
    except Exception as e:
        print(f"⚠️  Error following redirect for {share_url}: {e}")
        return share_url


def resolve_all_urls(urls: List[str]) -> List[str]:
    """Resolve all Facebook share URLs to direct video URLs"""
    print(f"\n🔍 Resolving {len(urls)} Facebook share URLs...")
    resolved_urls = []
    
    for i, url in enumerate(urls, 1):
        print(f"  [{i}/{len(urls)}] Resolving: {url[:60]}...")
        
        # First try to extract video ID and construct watch URL
        resolved = resolve_facebook_url(url)
        
        # If that didn't change the URL, try following redirects
        if resolved == url:
            resolved = resolve_urls_with_redirect(url)
        
        resolved_urls.append(resolved)
        
        if resolved != url:
            print(f"      ✅ Resolved to: {resolved[:70]}...")
        else:
            print(f"      ⚠️  Could not resolve, using original URL")
    
    return resolved_urls


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
    print(f"⚙️  Quality: {quality}\n")
    
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
        start_time = time.time()
        
        response = requests.post(
            API_ENDPOINT,
            json=request_data,
            headers=headers,
            timeout=600  # 10 minute timeout for batch operations
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Batch download completed in {elapsed_time:.2f} seconds\n")
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
        
        # Truncate URL for display
        url_display = url[:70] + "..." if len(url) > 70 else url
        print(f"\n[{i}/{len(results)}] {url_display}")
        print(f"   Status: {status}")
        print(f"   Content Type: {content_type}")
        print(f"   Session ID: {session_id}")
        
        if status == "completed" and download_url:
            print(f"   ✅ Download URL: {API_BASE_URL}{download_url}")
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
    print("=" * 80)


def main():
    """Main function"""
    print("🚀 Facebook Batch Video Downloader v2 (with URL Resolution)")
    print("=" * 80)
    
    # Check API health
    print(f"🔍 Checking API health at {API_BASE_URL}...")
    if not check_api_health():
        print(f"\n❌ API is not accessible at {API_BASE_URL}")
        print("\n💡 Please make sure the backend is running:")
        print("   cd app/api && ./start_api.sh")
        print("   OR")
        print("   cd app/api && uvicorn app.main:app --reload")
        sys.exit(1)
    
    print("✅ API is running and accessible\n")
    
    # Resolve URLs first
    resolved_urls = resolve_all_urls(FACEBOOK_URLS)
    
    # Download all videos
    results = download_facebook_batch(resolved_urls, quality="high")
    
    # Print results
    if results:
        print_results(results, FACEBOOK_URLS)
    else:
        print("\n⚠️  No results returned from the API")
    
    print("\n🎯 Batch download process completed!")


if __name__ == "__main__":
    main()

