#!/usr/bin/env python3
"""
Test script for Sora 2 video extraction and watermark removal
This script tests if yt-dlp can extract Sora 2 videos and what formats are available
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'api'))

from app.services.sora import SoraService


async def test_sora_extraction():
    """Test Sora video extraction with various URLs"""

    # Initialize the Sora service
    sora_service = SoraService()

    # Test URLs - these are example URLs, you'll need real Sora 2 URLs
    test_urls = [
        # Real Sora 2 URL for testing
        "https://sora.chatgpt.com/p/s_68dff2dd31348191bd168e6a0ac8860e",
        # Add more real Sora 2 URLs here for testing
        # "https://sora.openai.com/video/example-id",
        # "https://openai.com/sora/example-id",
    ]

    print("🔍 Testing Sora 2 Video Extraction")
    print("=" * 50)

    if not test_urls:
        print("⚠️  No test URLs provided. Please add real Sora 2 URLs to test.")
        print("\nTo test with a real Sora 2 video:")
        print("1. Get a Sora 2 video URL")
        print("2. Add it to the test_urls list in this script")
        print("3. Run the script again")
        return

    for url in test_urls:
        print(f"\n📹 Testing URL: {url}")
        print("-" * 30)

        try:
            # Test extraction to see what formats are available
            result = await sora_service.test_sora_extraction(url)

            print(f"✅ Successfully extracted video info")
            print(f"   Title: {result.get('title', 'Unknown')}")
            print(f"   Extractor: {result.get('extractor', 'Unknown')}")
            print(f"   Duration: {result.get('duration', 0)} seconds")
            print(f"   Uploader: {result.get('uploader', 'Unknown')}")

            # Check available formats
            formats = result.get('formats', [])
            if formats:
                print(f"   📋 Available formats: {len(formats)}")
                for i, fmt in enumerate(formats[:5]):  # Show first 5 formats
                    print(
                        f"      {i+1}. {fmt.get('ext', 'unknown')} - {fmt.get('format_note', 'No note')} - {fmt.get('resolution', 'unknown resolution')}")

                # Check for no-watermark versions
                no_watermark_formats = [
                    f for f in formats if 'no_watermark' in f.get('format_note', '').lower()]
                if no_watermark_formats:
                    print(
                        f"   🎯 Found {len(no_watermark_formats)} no-watermark formats!")
                else:
                    print("   ⚠️  No explicit no-watermark formats found")
            else:
                print("   ❌ No formats found")

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            print(f"   This might mean:")
            print(f"   - URL is not accessible")
            print(f"   - yt-dlp doesn't support this Sora URL format")
            print(f"   - Authentication is required")


async def test_sora_download():
    """Test actual Sora video download"""

    sora_service = SoraService()

    # Test URLs - add real Sora 2 URLs here
    test_urls = [
        # Add real Sora 2 URLs here for testing
    ]

    print("\n\n📥 Testing Sora 2 Video Download")
    print("=" * 50)

    if not test_urls:
        print("⚠️  No test URLs provided for download testing.")
        return

    for url in test_urls:
        print(f"\n📹 Testing download: {url}")
        print("-" * 30)

        try:
            result = await sora_service.download_video(url, "high")

            print(f"✅ Download successful!")
            print(f"   Session ID: {result.get('session_id')}")
            print(f"   Status: {result.get('status')}")
            print(f"   Download URL: {result.get('download_url')}")
            print(f"   Description: {result.get('description')}")
            print(f"   Author: {result.get('author')}")

        except Exception as e:
            print(f"   ❌ Download failed: {str(e)}")


def print_instructions():
    """Print instructions for using this test script"""
    print("\n" + "=" * 60)
    print("🎬 SORA 2 WATERMARK REMOVAL TEST SCRIPT")
    print("=" * 60)
    print()
    print("This script tests if your app can extract and download Sora 2 videos")
    print("without watermarks, similar to how it handles TikTok videos.")
    print()
    print("📋 To use this script:")
    print("1. Get a real Sora 2 video URL (from sora.openai.com)")
    print("2. Edit this script and add the URL to the test_urls list")
    print("3. Run: python test_sora.py")
    print()
    print("🔍 What this tests:")
    print("• Whether yt-dlp can extract Sora 2 video information")
    print("• What video formats are available")
    print("• Whether no-watermark versions exist")
    print("• If the download process works")
    print()
    print("📝 Example Sora 2 URL formats to try:")
    print("• https://sora.openai.com/video/[video-id]")
    print("• https://openai.com/sora/[video-id]")
    print()


async def main():
    """Main test function"""
    print_instructions()

    # Test extraction first
    await test_sora_extraction()

    # Test download if URLs are provided
    await test_sora_download()

    print("\n" + "=" * 60)
    print("✅ Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
