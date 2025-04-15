import os
import yt_dlp


def download_tiktok_video(url):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'mp4',
        'quiet': False,
        'noplaylist': True
    }

    try:
        print(f"🔍 Downloading TikTok video from: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Download completed!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    url = input("Paste the TikTok video URL: ").strip()
    download_tiktok_video(url)
