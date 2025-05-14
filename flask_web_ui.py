import os
import yt_dlp
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import tempfile
import shutil
import uuid
import threading
import time
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tiktok-downloader-secret-key'
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['DOWNLOAD_FOLDER'] = 'downloads'

os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Store active downloads
active_downloads = {}
completed_downloads = []

DOWNLOAD_LIFESPAN_MINUTES = 5
CLEANUP_INTERVAL_SECONDS = 60

def download_tiktok_video(url, output_dir):
    filename = f"tiktok_{uuid.uuid4().hex[:8]}.mp4"
    output_path = os.path.join(output_dir, filename)

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'mp4',
        'quiet': False,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return {
                'filename': filename,
                'title': info.get('title', 'Unknown'),
                'url': url,
                'timestamp': datetime.now(),
                'success': True
            }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'success': False
        }


def process_url_list(urls, session_id):
    global active_downloads, completed_downloads
    active_downloads[session_id]['status'] = 'processing'
    results = []

    for i, url_item in enumerate(urls):
        active_downloads[session_id]['progress'] = int((i / len(urls)) * 100)
        active_downloads[session_id]['current_url'] = url_item

        result = download_tiktok_video(url_item, app.config['DOWNLOAD_FOLDER'])
        results.append(result)

        if result['success']:
            completed_downloads.append(result)

    active_downloads[session_id]['status'] = 'completed'
    active_downloads[session_id]['progress'] = 100
    active_downloads[session_id]['results'] = results


def cleanup_old_downloads():
    global completed_downloads
    while True:
        now = datetime.now()
        for download_info in list(completed_downloads):
            if now - download_info['timestamp'] > timedelta(minutes=DOWNLOAD_LIFESPAN_MINUTES):
                file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], download_info['filename'])
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Deleted old file: {download_info['filename']}")
                    completed_downloads.remove(download_info)
                except Exception as e:
                    print(f"Error deleting file {download_info['filename']} or removing from list: {e}")
        
        time.sleep(CLEANUP_INTERVAL_SECONDS)


@app.route('/')
def index():
    return render_template('index.html', active_downloads=active_downloads, completed_downloads=completed_downloads)


@app.route('/download', methods=['POST'])
def download():
    if 'url' in request.form and request.form['url'].strip():
        # Single URL download
        url_input = request.form['url'].strip()
        session_id = str(uuid.uuid4())

        active_downloads[session_id] = {
            'type': 'single',
            'urls': [url_input],
            'status': 'starting',
            'progress': 0,
            'current_url': url_input
        }

        thread = threading.Thread(
            target=process_url_list, args=([url_input], session_id))
        thread.daemon = True
        thread.start()

        flash('Download started!', 'success')

    elif 'url_file' in request.files and request.files['url_file'].filename:
        # File upload with multiple URLs
        file = request.files['url_file']
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path)

        with open(temp_path, 'r') as f:
            urls_input = [line.strip() for line in f.readlines() if line.strip()]

        if urls_input:
            session_id = str(uuid.uuid4())
            active_downloads[session_id] = {
                'type': 'batch',
                'urls': urls_input,
                'status': 'starting',
                'progress': 0,
                'current_url': ''
            }

            thread = threading.Thread(
                target=process_url_list, args=(urls_input, session_id))
            thread.daemon = True
            thread.start()

            flash(f'Batch download started with {len(urls_input)} URLs!', 'success')
        else:
            flash('No valid URLs found in file.', 'error')
    else:
        flash('Please provide a URL or upload a file with URLs.', 'error')

    return redirect(url_for('index'))


@app.route('/status/<session_id>')
def status(session_id):
    if session_id in active_downloads:
        return active_downloads[session_id]
    return {'error': 'Download session not found'}, 404


@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)


# Create templates directory and index.html
os.makedirs('templates', exist_ok=True)

with open('templates/index.html', 'w') as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikSave - Download TikTok Videos Without Watermark</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        tiktok: {
                            primary: '#00f2ea',
                            secondary: '#ff0050',
                            dark: '#010101',
                            light: '#ffffff'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        .bg-gradient-tiktok {
            background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        }
        .bg-gradient-purple {
            background: linear-gradient(135deg, #C4B5FD 0%, #8B5CF6 50%, #4C1D95 100%);
        }
    </style>
</head>
<body class="min-h-screen bg-gradient-to-br from-tiktok-light via-white to-tiktok-secondary/20 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <header class="sticky top-0 z-50 bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm shadow-sm">
        <div class="container mx-auto px-4 py-4 flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <svg class="w-8 h-8 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
                <span class="text-xl font-bold bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent">
                    TikSave
                </span>
            </div>
        </div>
    </header>

    <main class="container mx-auto px-4 py-8">
        <div class="max-w-3xl mx-auto">
            <h1 class="text-3xl md:text-4xl font-bold mb-6 text-center bg-gradient-to-r from-teal-600 to-purple-600 bg-clip-text text-transparent">
                TikTok Video Downloader
            </h1>
            <p class="text-lg text-gray-700 dark:text-gray-300 mb-10 text-center">
                Download TikTok videos without watermark, quickly and easily. Files are available for 5 minutes.
            </p>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="mb-4 p-4 rounded-lg {% if category == 'success' %}bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400{% else %}bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400{% endif %}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden p-6 mb-8">
                <div class="space-y-6">
                    <!-- Single Video Download -->
                    <div>
                        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Single Video Download</h2>
                        <form action="/download" method="post" class="space-y-4">
                            <div>
                                <label for="url" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">TikTok URL</label>
                                <input type="url" id="url" name="url" 
                                    class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-teal-500 dark:focus:ring-teal-400"
                                    placeholder="https://www.tiktok.com/@user/video/1234567890" required>
                            </div>
                            <button type="submit" 
                                class="w-full bg-gradient-to-r from-teal-500 to-purple-500 hover:from-teal-600 hover:to-purple-600 text-white font-medium py-2 px-4 rounded-lg shadow-sm transition-all duration-200">
                                Download Video
                            </button>
                        </form>
                    </div>

                    <!-- Batch Download -->
                    <div class="pt-6 border-t border-gray-200 dark:border-gray-700">
                        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Batch Download</h2>
                        <form action="/download" method="post" enctype="multipart/form-data" class="space-y-4">
                            <div>
                                <label for="url_file" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Upload URL List</label>
                                <input type="file" id="url_file" name="url_file" accept=".txt"
                                    class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-teal-500 dark:focus:ring-teal-400">
                                <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Upload a text file with one URL per line</p>
                            </div>
                            <button type="submit" 
                                class="w-full bg-gradient-to-r from-teal-500 to-purple-500 hover:from-teal-600 hover:to-purple-600 text-white font-medium py-2 px-4 rounded-lg shadow-sm transition-all duration-200">
                                Start Batch Download
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Active Downloads -->
            {% if active_downloads %}
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden p-6 mb-8">
                <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Active Downloads</h2>
                <div class="space-y-4">
                    {% for id, download_item in active_downloads.items() %}
                    {% if download_item.status != 'completed' %}
                    <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                        <div class="flex justify-between items-center mb-2">
                            <h3 class="font-medium text-gray-900 dark:text-white">{{ download_item.type|capitalize }} Download</h3>
                            <span class="text-sm text-gray-500 dark:text-gray-400">{{ download_item.status|capitalize }}</span>
                        </div>
                        <p class="text-sm text-gray-600 dark:text-gray-300 mb-2">{{ download_item.current_url }}</p>
                        <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                            <div class="bg-gradient-to-r from-teal-500 to-purple-500 h-2 rounded-full transition-all duration-500" style="width: {{ download_item.progress }}%"></div>
                        </div>
                    </div>
                    {% endif %}
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <!-- Completed Downloads -->
            <div id="completed-downloads-section" class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden p-6 {% if not completed_downloads %}hidden{% endif %}">
                <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Completed Downloads (Available for 5 mins)</h2>
                {% if not completed_downloads %}
                    <p class="text-gray-600 dark:text-gray-400">No downloads available. They will appear here once completed and will be removed after 5 minutes.</p>
                {% else %}
                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead>
                            <tr class="text-left border-b border-gray-200 dark:border-gray-700">
                                <th class="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400">Title</th>
                                <th class="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400">URL</th>
                                <th class="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for download_item in completed_downloads %}
                            <tr class="border-b border-gray-100 dark:border-gray-700">
                                <td class="py-3 text-sm text-gray-900 dark:text-white">{{ download_item.title }}</td>
                                <td class="py-3 text-sm text-gray-600 dark:text-gray-300">
                                    <a href="{{ download_item.url }}" target="_blank" class="hover:text-teal-600 dark:hover:text-teal-400">
                                        {{ download_item.url[:30] }}...
                                    </a>
                                </td>
                                <td class="py-3">
                                    <a href="/downloads/{{ download_item.filename }}" 
                                        class="inline-flex items-center px-3 py-1 rounded-lg text-sm font-medium text-white bg-gradient-to-r from-teal-500 to-purple-500 hover:from-teal-600 hover:to-purple-600 transition-all duration-200">
                                        Download
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% endif %}
            </div>
        </div>
    </main>

    <footer class="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 mt-12">
        <div class="container mx-auto px-4 py-8">
            <div class="text-center">
                <p class="text-sm text-gray-600 dark:text-gray-400">
                    Made with ❤️ for TikTok content creators and fans
                </p>
            </div>
        </div>
    </footer>

    <script>
        function hasActiveProcessingDownloads() {
            const activeDownloadsElement = document.querySelector('.bg-gray-50.dark\\\\:bg-gray-700');
            return activeDownloadsElement !== null;
        }

        function hasVisibleCompletedDownloads() {
            const completedSection = document.getElementById('completed-downloads-section');
            if (!completedSection || completedSection.classList.contains('hidden')) {
                return false;
            }
            return completedSection.querySelectorAll('tbody tr').length > 0;
        }

        if (hasActiveProcessingDownloads() || hasVisibleCompletedDownloads()) {
            setTimeout(function() {
                window.location.reload();
            }, 7000);
        }

        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
        }
    </script>
</body>
</html>''')

if __name__ == '__main__':
    print("🌐 Starting Flask Web UI for TikTok Downloader")
    cleanup_thread = threading.Thread(target=cleanup_old_downloads, daemon=True)
    cleanup_thread.start()
    print(f"🗑️  Auto-cleanup for files older than {DOWNLOAD_LIFESPAN_MINUTES} minutes started (checks every {CLEANUP_INTERVAL_SECONDS}s).")

    app.run(debug=True, host='0.0.0.0', port=5000)
