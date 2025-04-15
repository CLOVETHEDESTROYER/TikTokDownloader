import os
import csv
import datetime
import yt_dlp


def download_instagram_content(url, output_dir="downloads/instagram", csv_log=True):
    os.makedirs(output_dir, exist_ok=True)

    video_info = {}

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'best',
        'quiet': False,
        'noplaylist': False,  # Set to False to handle carousel posts
        'cookiefile': 'instagram_cookies.txt',  # Optional for private content
        'extract_flat': False,
        'ignoreerrors': True
    }

    try:
        print(f"🔍 Downloading Instagram content from: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Handle carousel posts and single posts differently
            if 'entries' in info and info['entries']:
                # For carousel posts, process each item
                print(
                    f"📱 Found carousel post with {len(info['entries'])} items")
                all_info = []

                for i, entry in enumerate(info['entries'], 1):
                    entry_info = {
                        'title': entry.get('title', f'Instagram Post {i}'),
                        'uploader': entry.get('uploader', 'Unknown'),
                        'description': entry.get('description', ''),
                        'upload_date': entry.get('upload_date', ''),
                        'duration': entry.get('duration', 0),
                        'like_count': entry.get('like_count', 0),
                        'comment_count': entry.get('comment_count', 0),
                        'view_count': entry.get('view_count', 0),
                        'filename': f"{entry.get('title', f'instagram_post_{i}')}.{entry.get('ext', 'mp4')}",
                        'url': url,
                        'type': 'carousel_item',
                        'carousel_index': i,
                        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    all_info.append(entry_info)

                # Now download all items
                ydl.download([url])

                # Log each item to CSV
                if csv_log:
                    for entry_info in all_info:
                        log_to_csv(entry_info, csv_file=os.path.join(
                            output_dir, "instagram_downloads.csv"))

                return all_info

            else:
                # For single posts
                video_info = {
                    'title': info.get('title', 'Instagram Post'),
                    'uploader': info.get('uploader', 'Unknown'),
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date', ''),
                    'duration': info.get('duration', 0),
                    'like_count': info.get('like_count', 0),
                    'comment_count': info.get('comment_count', 0),
                    'view_count': info.get('view_count', 0),
                    'filename': f"{info.get('title', 'instagram_post')}.{info.get('ext', 'mp4')}",
                    'url': url,
                    'type': 'single_post',
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Download the video
                ydl.download([url])

                # Log to CSV if enabled
                if csv_log:
                    log_to_csv(video_info, csv_file=os.path.join(
                        output_dir, "instagram_downloads.csv"))

                return video_info

        print("✅ Download completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def log_to_csv(content_info, csv_file="downloads/instagram/instagram_downloads.csv"):
    """Log content metadata to a CSV file"""
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    # Check if file exists to determine if we need to write headers
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=content_info.keys())

        # Write header only if file is new
        if not file_exists:
            writer.writeheader()

        writer.writerow(content_info)

    print(f"📊 Metadata logged to {csv_file}")


def read_urls_from_file(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return []

    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def batch_download(file_path="instagram_urls.txt"):
    urls = read_urls_from_file(file_path)
    if not urls:
        print("⚠️ No URLs found.")
        return

    for url in urls:
        download_instagram_content(url)


if __name__ == "__main__":
    print("📱 Instagram Content Downloader with CSV Export 📊")
    print("1. Download single post/reel")
    print("2. Batch download from file")
    choice = input("Select an option (1/2): ").strip()

    if choice == "1":
        url = input("Paste the Instagram post/reel URL: ").strip()
        download_instagram_content(url)
    elif choice == "2":
        file_path = input(
            "Enter path to URL file (default: instagram_urls.txt): ").strip()
        if not file_path:
            file_path = "instagram_urls.txt"
        batch_download(file_path)
    else:
        print("❌ Invalid choice!")
