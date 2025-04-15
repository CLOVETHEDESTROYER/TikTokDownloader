# TikTokDownloader
# 📥 TikTok Video Scraper & Downloader

This project allows you to download TikTok videos (often without watermark) using Python and the powerful `yt-dlp` library.

---

## 🚀 Features

- ✅ Download single or multiple TikTok videos
- ✅ Save videos in high quality
- ✅ Automatically name and organize files
- ✅ Extendable for GUI, Web, or Cloud sync

---

## 🧰 Requirements

Install Python libraries:

```bash
pip install yt-dlp
```

Optionally, create a folder for downloads:

```bash
mkdir downloads
```

---

## 📝 Step-by-Step Instructions

### Step 1: Single Video Downloader

Create a Python file named `tiktok_downloader.py`:

```python
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
```

---

### Step 2: Batch Video Downloader

Create a text file `tiktok_urls.txt` with one TikTok link per line:

```
https://www.tiktok.com/@user/video/1234567890
https://www.tiktok.com/@user/video/2345678901
```

Then create a new Python file `batch_tiktok_downloader.py`:

```python
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
```

---

## 📁 File Structure

```
tiktok_downloader/
├── downloads/
├── tiktok_downloader.py
├── batch_tiktok_downloader.py
└── tiktok_urls.txt
```

---

## 🔧 Next Steps (Optional Features)

| Feature                    | Description |
|----------------------------|-------------|
| 🧪 Watermark detection     | Auto-detect if watermark is present |
| 📊 CSV export              | Log downloaded file names and metadata |
| 🌐 Flask Web UI            | Upload text file via browser and start download |
| 🎮 GUI (Tkinter)           | User-friendly interface for file input and download |
| ☁️ Dropbox / GDrive Upload | Auto-sync to cloud after download |
| 📱 Telegram Bot            | Download videos via chat commands |

---


---

