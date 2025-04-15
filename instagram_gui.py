import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
import datetime
import csv


class InstagramDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Content Downloader")
        self.root.geometry("650x550")
        self.root.resizable(True, True)

        # Set app theme
        self.root.configure(bg="#f0f0f0")

        # Create download folder if it doesn't exist
        self.download_dir = "downloads/instagram"
        os.makedirs(self.download_dir, exist_ok=True)

        # Variables
        self.url_var = tk.StringVar()
        self.file_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0)
        self.csv_export_var = tk.BooleanVar(value=True)
        self.carousel_status_var = tk.StringVar(value="")

        # Create UI elements
        self.create_widgets()

        # Active download flag
        self.download_in_progress = False

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=10)

        title_label = ttk.Label(
            title_frame,
            text="📸 Instagram Content Downloader",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack()

        # Tabs for different download options
        tab_control = ttk.Notebook(main_frame)

        # Single Download Tab
        single_tab = ttk.Frame(tab_control)
        tab_control.add(single_tab, text="Single Post/Reel")

        # Batch Download Tab
        batch_tab = ttk.Frame(tab_control)
        tab_control.add(batch_tab, text="Batch Download")

        # Options Tab
        options_tab = ttk.Frame(tab_control)
        tab_control.add(options_tab, text="Options")

        tab_control.pack(expand=True, fill=tk.BOTH, pady=10)

        # Single Download Tab Content
        url_frame = ttk.Frame(single_tab, padding=10)
        url_frame.pack(fill=tk.X, pady=5)

        url_label = ttk.Label(url_frame, text="Instagram Post/Reel URL:")
        url_label.pack(anchor=tk.W)

        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.pack(fill=tk.X, pady=5)

        download_btn = ttk.Button(
            url_frame,
            text="Download Content",
            command=self.download_single
        )
        download_btn.pack(anchor=tk.E, pady=5)

        # Batch Download Tab Content
        file_frame = ttk.Frame(batch_tab, padding=10)
        file_frame.pack(fill=tk.X, pady=5)

        file_label = ttk.Label(file_frame, text="Instagram URLs File (.txt):")
        file_label.pack(anchor=tk.W)

        file_entry_frame = ttk.Frame(file_frame)
        file_entry_frame.pack(fill=tk.X, pady=5)

        file_entry = ttk.Entry(
            file_entry_frame, textvariable=self.file_path_var, width=40)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_btn = ttk.Button(
            file_entry_frame,
            text="Browse",
            command=self.browse_file
        )
        browse_btn.pack(side=tk.RIGHT, padx=5)

        batch_download_btn = ttk.Button(
            file_frame,
            text="Download All Content",
            command=self.download_batch
        )
        batch_download_btn.pack(anchor=tk.E, pady=5)

        # Options Tab Content
        options_frame = ttk.Frame(options_tab, padding=10)
        options_frame.pack(fill=tk.X, pady=5)

        csv_check = ttk.Checkbutton(
            options_frame,
            text="Export metadata to CSV",
            variable=self.csv_export_var
        )
        csv_check.pack(anchor=tk.W, pady=5)

        cookie_frame = ttk.LabelFrame(
            options_frame, text="Authentication", padding=10)
        cookie_frame.pack(fill=tk.X, pady=10)

        cookie_label = ttk.Label(
            cookie_frame,
            text="This app uses instagram_cookies.txt for private content.\nTo access private posts, please ensure this file contains valid Instagram cookies."
        )
        cookie_label.pack(pady=5)

        cookie_status = ttk.Label(
            cookie_frame,
            text=f"Cookie file: {'Found' if os.path.exists('instagram_cookies.txt') else 'Not found'}"
        )
        cookie_status.pack(pady=5)

        # Status and Progress Frame
        status_frame = ttk.LabelFrame(
            main_frame, text="Download Status", padding=10)
        status_frame.pack(fill=tk.X, pady=10)

        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)

        carousel_label = ttk.Label(
            status_frame, textvariable=self.carousel_status_var)
        carousel_label.pack(anchor=tk.W, pady=2)

        progress = ttk.Progressbar(
            status_frame,
            variable=self.progress_var,
            length=100,
            mode='determinate'
        )
        progress.pack(fill=tk.X, pady=5)

        # Output Folder Frame
        folder_frame = ttk.Frame(main_frame, padding=5)
        folder_frame.pack(fill=tk.X)

        folder_label = ttk.Label(
            folder_frame,
            text=f"Downloads folder: {os.path.abspath(self.download_dir)}"
        )
        folder_label.pack(side=tk.LEFT)

        open_folder_btn = ttk.Button(
            folder_frame,
            text="Open Folder",
            command=self.open_download_folder
        )
        open_folder_btn.pack(side=tk.RIGHT)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

    def open_download_folder(self):
        download_path = os.path.abspath(self.download_dir)
        if os.path.exists(download_path):
            os.startfile(download_path) if os.name == 'nt' else os.system(
                f'open "{download_path}"')
        else:
            messagebox.showerror("Error", "Download folder does not exist!")

    def download_single(self):
        if self.download_in_progress:
            messagebox.showinfo(
                "Info", "Download already in progress. Please wait.")
            return

        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter an Instagram URL.")
            return

        thread = threading.Thread(
            target=self._download_single_thread, args=(url,))
        thread.daemon = True
        thread.start()

    def _download_single_thread(self, url):
        self.download_in_progress = True
        self.status_var.set(f"Processing: {url}")
        self.carousel_status_var.set("")
        self.progress_var.set(0)

        try:
            ydl_opts = {
                'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                'format': 'best',
                'quiet': False,
                'noplaylist': False,  # Set to False to handle carousel posts
                'cookiefile': 'instagram_cookies.txt' if os.path.exists('instagram_cookies.txt') else None,
                'extract_flat': False,
                'ignoreerrors': True,
                'progress_hooks': [self._progress_hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # First, extract info without downloading
                info = ydl.extract_info(url, download=False)

                # Check if it's a carousel post
                if 'entries' in info and info['entries']:
                    carousel_count = len(info['entries'])
                    self.carousel_status_var.set(
                        f"📱 Carousel post with {carousel_count} items")

                    # Prepare metadata for each item
                    all_info = []
                    for i, entry in enumerate(info['entries'], 1):
                        entry_info = {
                            'title': entry.get('title', f'Instagram Post {i}'),
                            'uploader': entry.get('uploader', 'Unknown'),
                            'description': entry.get('description', ''),
                            'upload_date': entry.get('upload_date', ''),
                            'filename': ydl.prepare_filename(entry),
                            'url': url,
                            'type': 'carousel_item',
                            'carousel_index': i,
                            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        all_info.append(entry_info)

                    # Now download the entire carousel
                    self.status_var.set(
                        f"Downloading carousel: {info.get('title', 'Unknown')}")
                    ydl.download([url])

                    # Log each item to CSV if enabled
                    if self.csv_export_var.get():
                        for entry_info in all_info:
                            self._log_to_csv(entry_info)

                    self.status_var.set(
                        f"Completed: {carousel_count} items from carousel")

                else:
                    # Single post
                    filename = ydl.prepare_filename(info)
                    self.status_var.set(
                        f"Downloading: {info.get('title', 'Unknown')}")

                    # Download the content
                    ydl.download([url])

                    # Log to CSV if enabled
                    if self.csv_export_var.get():
                        video_info = {
                            'title': info.get('title', 'Instagram Post'),
                            'uploader': info.get('uploader', 'Unknown'),
                            'description': info.get('description', ''),
                            'upload_date': info.get('upload_date', ''),
                            'filename': filename,
                            'url': url,
                            'type': 'single_post',
                            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        self._log_to_csv(video_info)

                    self.status_var.set(
                        f"Download completed: {os.path.basename(filename)}")

            self.progress_var.set(100)
            messagebox.showinfo("Success", "Content downloaded successfully!")

        except Exception as e:
            self.status_var.set(f"Error: {str(e)[:50]}...")
            self.carousel_status_var.set("")
            messagebox.showerror("Download Error", str(e))

        finally:
            self.download_in_progress = False

    def download_batch(self):
        if self.download_in_progress:
            messagebox.showinfo(
                "Info", "Download already in progress. Please wait.")
            return

        file_path = self.file_path_var.get().strip()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid file.")
            return

        try:
            with open(file_path, 'r') as file:
                urls = [line.strip()
                        for line in file.readlines() if line.strip()]

            if not urls:
                messagebox.showinfo("Info", "No URLs found in the file.")
                return

            thread = threading.Thread(
                target=self._download_batch_thread, args=(urls,))
            thread.daemon = True
            thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Could not read the file: {str(e)}")

    def _download_batch_thread(self, urls):
        self.download_in_progress = True
        total_urls = len(urls)
        successful_downloads = 0

        for i, url in enumerate(urls, 1):
            try:
                progress_percent = (i - 1) / total_urls * 100
                self.progress_var.set(progress_percent)
                self.status_var.set(f"Downloading {i}/{total_urls}: {url}")
                self.carousel_status_var.set("")

                ydl_opts = {
                    'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                    'format': 'best',
                    'quiet': False,
                    'noplaylist': False,
                    'cookiefile': 'instagram_cookies.txt' if os.path.exists('instagram_cookies.txt') else None,
                    'extract_flat': False,
                    'ignoreerrors': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Check if it's a carousel post
                    info = ydl.extract_info(url, download=False)

                    if 'entries' in info and info['entries']:
                        carousel_count = len(info['entries'])
                        self.carousel_status_var.set(
                            f"📱 Carousel post with {carousel_count} items")

                        # Process carousel metadata
                        all_info = []
                        for j, entry in enumerate(info['entries'], 1):
                            entry_info = {
                                'title': entry.get('title', f'Instagram Post {j}'),
                                'uploader': entry.get('uploader', 'Unknown'),
                                'description': entry.get('description', ''),
                                'upload_date': entry.get('upload_date', ''),
                                'url': url,
                                'type': 'carousel_item',
                                'carousel_index': j,
                                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            all_info.append(entry_info)

                    # Download content
                    ydl.download([url])
                    successful_downloads += 1

                    # Log to CSV if enabled
                    if self.csv_export_var.get():
                        if 'entries' in info and info['entries']:
                            for entry_info in all_info:
                                self._log_to_csv(entry_info)
                        else:
                            video_info = {
                                'title': info.get('title', 'Instagram Post'),
                                'uploader': info.get('uploader', 'Unknown'),
                                'description': info.get('description', ''),
                                'upload_date': info.get('upload_date', ''),
                                'url': url,
                                'type': 'single_post',
                                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            self._log_to_csv(video_info)

            except Exception as e:
                print(f"Error downloading {url}: {str(e)}")

        self.progress_var.set(100)
        self.status_var.set(
            f"Batch download completed: {successful_downloads}/{total_urls} items")
        self.carousel_status_var.set("")
        messagebox.showinfo(
            "Success", f"Downloaded {successful_downloads} out of {total_urls} items.")
        self.download_in_progress = False

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            # Extract download percentage if available
            if 'total_bytes' in d and d['total_bytes'] > 0:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                self.progress_var.set(percent)
            elif 'downloaded_bytes' in d:
                # If we don't have total_bytes, just show activity
                current_val = self.progress_var.get()
                self.progress_var.set((current_val + 1) % 100)

            self.status_var.set(f"Downloading: {d.get('filename', 'Unknown')}")

        elif d['status'] == 'finished':
            self.status_var.set(
                f"Finished file: {os.path.basename(d.get('filename', 'Unknown'))}")

    def _log_to_csv(self, content_info, csv_file=None):
        """Log content metadata to a CSV file"""
        if csv_file is None:
            csv_file = os.path.join(
                self.download_dir, "instagram_downloads.csv")

        os.makedirs(os.path.dirname(csv_file), exist_ok=True)

        # Check if file exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=content_info.keys())

            # Write header only if file is new
            if not file_exists:
                writer.writeheader()

            writer.writerow(content_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramDownloaderGUI(root)
    root.mainloop()
