#!/usr/bin/env python3
import requests
import json
import argparse


def test_tiktok_endpoint(api_url, api_key, video_url):
    """Test the TikTok download endpoint"""
    print(f"\n🧪 Testing TikTok endpoint with URL: {video_url}")

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }

    data = {
        "url": video_url,
        "quality": "best"
    }

    endpoint = f"{api_url}/api/v1/tiktok/download"
    print(f"🔗 Endpoint: {endpoint}")

    response = requests.post(
        endpoint,
        headers=headers,
        json=data
    )

    print(f"📊 Status Code: {response.status_code}")

    try:
        result = response.json()
        print("📋 Response:")
        print(json.dumps(result, indent=2))

        if response.status_code == 200 and "download_url" in result:
            print(
                f"✅ SUCCESS: Video available at {api_url}{result['download_url']}")
            return True
        else:
            print("❌ FAILED: Couldn't download TikTok video")
            return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_instagram_endpoint(api_url, api_key, post_url):
    """Test the Instagram download endpoint"""
    print(f"\n🧪 Testing Instagram endpoint with URL: {post_url}")

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }

    data = {
        "url": post_url,
        "quality": "best"
    }

    response = requests.post(
        f"{api_url}/api/v1/instagram/download",
        headers=headers,
        json=data
    )

    print(f"📊 Status Code: {response.status_code}")

    try:
        result = response.json()
        print("📋 Response:")
        print(json.dumps(result, indent=2))

        if response.status_code == 200 and "download_url" in result:
            print(
                f"✅ SUCCESS: Content available at {api_url}{result['download_url']}")
            return True
        else:
            print("❌ FAILED: Couldn't download Instagram content")
            return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Test TikTok and Instagram download endpoints')
    parser.add_argument(
        '--api-url', default='http://localhost:8000', help='API base URL')
    parser.add_argument('--api-key', default='test_api_key_123',
                        help='API key for authentication')
    parser.add_argument('--tiktok-url', help='TikTok video URL to test')
    parser.add_argument('--instagram-url', help='Instagram post URL to test')

    args = parser.parse_args()

    print("🔍 API Endpoint Tester")
    print(f"🌐 API URL: {args.api_url}")

    if args.tiktok_url:
        test_tiktok_endpoint(args.api_url, args.api_key, args.tiktok_url)

    if args.instagram_url:
        test_instagram_endpoint(args.api_url, args.api_key, args.instagram_url)

    if not args.tiktok_url and not args.instagram_url:
        print("\n⚠️ No URLs provided. Please provide at least one URL to test.")
        print("Example usage:")
        print("python test_endpoints.py --tiktok-url https://www.tiktok.com/@username/video/1234567890123456789")
        print(
            "python test_endpoints.py --instagram-url https://www.instagram.com/p/ABC123/")


if __name__ == "__main__":
    main()
