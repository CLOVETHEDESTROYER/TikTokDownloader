from app.services.tiktok import TikTokService
import asyncio
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


async def test_download():
    """Test downloading a TikTok video without watermark."""
    # Create TikTokService instance
    tiktok_service = TikTokService()

    # Test URL - replace with a real TikTok URL for testing
    test_url = "https://www.tiktok.com/@tiktok/video/7106594312292453674"

    try:
        logging.info(f"Testing download for URL: {test_url}")

        # Test no-watermark download
        result = await tiktok_service.download_video(test_url, "high")

        logging.info(f"Download successful!")
        logging.info(f"Result: {result}")

        # Check if file exists
        filename = result["download_url"].split("/")[-1]
        filepath = os.path.join(tiktok_service.download_path, filename)

        if os.path.exists(filepath):
            file_size = os.path.getsize(filepath)
            logging.info(f"Downloaded file: {filepath}")
            logging.info(f"File size: {file_size / (1024 * 1024):.2f} MB")
        else:
            logging.error(f"File not found: {filepath}")

    except Exception as e:
        logging.error(f"Error during download test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_download())
