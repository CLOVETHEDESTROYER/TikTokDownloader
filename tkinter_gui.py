import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp


class TikTokDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Video Downloader")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Set app icon and theme
        self.root.configure(bg="#f0f0f0")

        # Create download folder if it doesn't exist
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)

        # Variables
        self.url_var = tk.StringVar()
        self.file_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0)

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
            text="TikTok Video Downloader",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack()

        # Tabs for different download options
        tab_control = ttk.Notebook(main_frame)

        # Single Download Tab
        single_tab = ttk.Frame(tab_control)
        tab_control.add(single_tab, text="Single Video")

        # Batch Download Tab
        batch_tab = ttk.Frame(tab_control)
        tab_control.add(batch_tab, text="Batch Download")

        tab_control.pack(expand=True, fill=tk.BOTH, pady=10)

        # Single Download Tab Content
        url_frame = ttk.Frame(single_tab, padding=10)
        url_frame.pack(fill=tk.X, pady=5)

        url_label = ttk.Label(url_frame, text="TikTok Video URL:")
        url_label.pack(anchor=tk.W)

        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.pack(fill=tk.X, pady=5)

        download_btn = ttk.Button(
            url_frame,
            text="Download Video",
            command=self.download_single
        )
        download_btn.pack(anchor=tk.E, pady=5)

        # Batch Download Tab Content
        file_frame = ttk.Frame(batch_tab, padding=10)
        file_frame.pack(fill=tk.X, pady=5)

        file_label = ttk.Label(file_frame, text="TikTok URLs File (.txt):")
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
            text="Download All Videos",
            command=self.download_batch
        )
        batch_download_btn.pack(anchor=tk.E, pady=5)

        # Status and Progress Frame
        status_frame = ttk.LabelFrame(
            main_frame, text="Download Status", padding=10)
        status_frame.pack(fill=tk.X, pady=10)

        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)

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
            messagebox.showerror("Error", "Please enter a TikTok URL.")
            return

        thread = threading.Thread(
            target=self._download_single_thread, args=(url,))
        thread.daemon = True
        thread.start()

    def _download_single_thread(self, url):
        self.download_in_progress = True
        self.status_var.set(f"Downloading: {url}")
        self.progress_var.set(0)

        try:
            ydl_opts = {
                'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                'format': 'mp4',
                'quiet': False,
                'noplaylist': True,
                'progress_hooks': [self._progress_hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
                self.status_var.set(
                    f"Downloading: {info.get('title', 'Unknown')}")

                # Perform the download
                ydl.download([url])

            self.status_var.set(
                f"Download completed: {os.path.basename(filename)}")
            self.progress_var.set(100)
            messagebox.showinfo("Success", "Video downloaded successfully!")

        except Exception as e:
            self.status_var.set(f"Error: {str(e)[:50]}...")
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

        for i, url in enumerate(urls, 1):
            try:
                progress_percent = (i - 1) / total_urls * 100
                self.progress_var.set(progress_percent)
                self.status_var.set(f"Downloading {i}/{total_urls}: {url}")

                ydl_opts = {
                    'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                    'format': 'mp4',
                    'quiet': False,
                    'noplaylist': True
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            except Exception as e:
                print(f"Error downloading {url}: {str(e)}")

        self.progress_var.set(100)
        self.status_var.set(f"Batch download completed: {total_urls} videos")
        messagebox.showinfo("Success", f"Downloaded {total_urls} videos.")
        self.download_in_progress = False

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            # Extract download percentage
            if 'total_bytes' in d and d['total_bytes'] > 0:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                self.progress_var.set(percent)

            self.status_var.set(f"Downloading: {d.get('filename', 'Unknown')}")

        elif d['status'] == 'finished':
            self.status_var.set(
                f"Download finished: {d.get('filename', 'Unknown')}")
            self.progress_var.set(100)


if __name__ == "__main__":
    root = tk.Tk()
    app = TikTokDownloaderGUI(root)
    root.mainloop()
