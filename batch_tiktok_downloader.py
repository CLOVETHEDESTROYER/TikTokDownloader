import os
import yt_dlp


def read_urls_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []

    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def download_tiktok_video(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'mp4',
        'quiet': False,
        'noplaylist': True
    }

    try:
        print(f"🔽 Downloading: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Success!")
    except Exception as e:
        print(f"❌ Failed to download {url} — Error: {e}")


def batch_download(file_path="tiktok_urls.txt"):
    urls = read_urls_from_file(file_path)
    if not urls:
        print("⚠️ No URLs found.")
        return

    for url in urls:
        download_tiktok_video(url)


if __name__ == "__main__":
    batch_download("tiktok_urls.txt")
