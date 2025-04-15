import os
import yt_dlp


def download_instagram_video(url):
    output_dir = "downloads/instagram"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'best',  # Instagram often has different format availability
        'quiet': False,
        'noplaylist': False,  # Set to False to handle carousel posts
        'cookiefile': 'instagram_cookies.txt',  # Optional for private content
        'extract_flat': False,
        'ignoreerrors': True,  # Continue on error (useful for carousels)
    }

    try:
        print(f"🔍 Downloading Instagram content from: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Download completed!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    url = input("Paste the Instagram post/reel/video URL: ").strip()
    download_instagram_video(url)
