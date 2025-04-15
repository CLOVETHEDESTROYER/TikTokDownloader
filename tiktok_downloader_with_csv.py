import os
import csv
import datetime
import yt_dlp


def download_tiktok_video(url, output_dir="downloads", csv_log=True):
    os.makedirs(output_dir, exist_ok=True)

    video_info = {}

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'mp4',
        'quiet': False,
        'noplaylist': True
    }

    try:
        print(f"🔍 Downloading TikTok video from: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_info = {
                'title': info.get('title', 'Unknown'),
                'uploader': info.get('uploader', 'Unknown'),
                'duration': info.get('duration', 0),
                'view_count': info.get('view_count', 0),
                'like_count': info.get('like_count', 0),
                'filename': f"{info.get('title', 'video')}.{info.get('ext', 'mp4')}",
                'url': url,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Now download the video
            ydl.download([url])

        print("✅ Download completed!")

        # Log to CSV if enabled
        if csv_log:
            log_to_csv(video_info)

        return video_info

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def log_to_csv(video_info, csv_file="downloads/tiktok_downloads.csv"):
    """Log video metadata to a CSV file"""
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    # Check if file exists to determine if we need to write headers
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=video_info.keys())

        # Write header only if file is new
        if not file_exists:
            writer.writeheader()

        writer.writerow(video_info)

    print(f"📊 Metadata logged to {csv_file}")


def read_urls_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []

    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def batch_download(file_path="tiktok_urls.txt"):
    urls = read_urls_from_file(file_path)
    if not urls:
        print("⚠️ No URLs found.")
        return

    for url in urls:
        download_tiktok_video(url)


if __name__ == "__main__":
    print("🎬 TikTok Downloader with CSV Export 📊")
    print("1. Download single video")
    print("2. Batch download from file")
    choice = input("Select an option (1/2): ").strip()

    if choice == "1":
        url = input("Paste the TikTok video URL: ").strip()
        download_tiktok_video(url)
    elif choice == "2":
        file_path = input(
            "Enter path to URL file (default: tiktok_urls.txt): ").strip()
        if not file_path:
            file_path = "tiktok_urls.txt"
        batch_download(file_path)
    else:
        print("❌ Invalid choice!")
