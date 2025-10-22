#!/usr/bin/env python3
"""
Simple test script to start the server and test Sora 2 functionality
"""

import subprocess
import sys
import time
import requests
import os


def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")

    # Change to the API directory
    api_dir = os.path.join(os.path.dirname(__file__), 'app', 'api')
    os.chdir(api_dir)

    # Start the server
    try:
        process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn',
            'app.main:app',
            '--host', '0.0.0.0',
            '--port', '8001',
            '--reload'
        ])

        print("✅ Server started successfully!")
        print("📡 API available at: http://localhost:8001")
        print("📚 API docs available at: http://localhost:8001/docs")
        print("🎬 Sora endpoints available at: http://localhost:8001/api/v1/sora/")
        print("\n" + "="*60)
        print("🧪 TESTING SORA 2 ENDPOINTS")
        print("="*60)

        # Wait a moment for server to start
        time.sleep(3)

        # Test the health endpoint
        test_health()

        # Test the Sora health endpoint
        test_sora_health()

        print("\n" + "="*60)
        print("✅ Basic tests completed!")
        print("="*60)
        print("\n📋 Next steps:")
        print("1. Visit http://localhost:3000/sora in your browser")
        print("2. Or test the API directly at http://localhost:8001/docs")
        print("3. Try the Sora endpoints with real Sora 2 URLs")
        print("\n🛑 Press Ctrl+C to stop the server")

        # Keep the server running
        process.wait()

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        process.terminate()
    except Exception as e:
        print(f"❌ Error starting server: {e}")


def test_health():
    """Test the basic health endpoint"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(
                f"⚠️  Health endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")


def test_sora_health():
    """Test the Sora health endpoint"""
    try:
        response = requests.get(
            "http://localhost:8001/api/v1/sora/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Sora health endpoint working")
            print(f"   Service: {data.get('service')}")
            print(
                f"   Watermark removal enabled: {data.get('watermark_removal_enabled')}")
        else:
            print(
                f"⚠️  Sora health endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Sora health endpoint test failed: {e}")


def test_sora_extraction():
    """Test Sora video extraction with a sample URL"""
    print("\n🧪 Testing Sora video extraction...")

    # This is a placeholder URL - you'll need a real Sora 2 URL
    test_url = "https://sora.openai.com/video/example-id"

    try:
        response = requests.post(
            "http://localhost:8001/api/v1/sora/test",
            json={"url": test_url},
            headers={"X-API-Key": "website_key_123"},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Sora extraction test completed")
            print(f"   URL: {data.get('url')}")
            print(f"   Extractor: {data.get('extractor')}")
            print(f"   Formats found: {len(data.get('formats', []))}")
        else:
            print(
                f"⚠️  Sora extraction test returned status {response.status_code}")
            print(f"   Response: {response.text}")

    except Exception as e:
        print(f"❌ Sora extraction test failed: {e}")
        print("   This is expected if you don't have a real Sora 2 URL")


if __name__ == "__main__":
    print("🎬 Sora 2 Watermark Removal Test Server")
    print("=" * 50)

    start_server()
