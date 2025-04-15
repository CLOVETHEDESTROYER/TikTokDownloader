import os
import yt_dlp


def read_urls_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []

    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def download_instagram_video(url, output_dir="downloads/instagram"):
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
        print(f"🔽 Downloading: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✅ Success!")
    except Exception as e:
        print(f"❌ Failed to download {url} — Error: {e}")


def batch_download(file_path="instagram_urls.txt"):
    urls = read_urls_from_file(file_path)
    if not urls:
        print("⚠️ No URLs found.")
        return

    for url in urls:
        download_instagram_video(url)


if __name__ == "__main__":
    file_path = input(
        "Enter path to URL file (default: instagram_urls.txt): ").strip()
    if not file_path:
        file_path = "instagram_urls.txt"
    batch_download(file_path)
