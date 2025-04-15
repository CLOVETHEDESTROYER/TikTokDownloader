import os
import yt_dlp
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import tempfile
import shutil
import uuid
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tiktok-downloader-secret-key'
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['DOWNLOAD_FOLDER'] = 'downloads'

os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Store active downloads
active_downloads = {}
completed_downloads = []


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

    for i, url in enumerate(urls):
        active_downloads[session_id]['progress'] = int((i / len(urls)) * 100)
        active_downloads[session_id]['current_url'] = url

        result = download_tiktok_video(url, app.config['DOWNLOAD_FOLDER'])
        results.append(result)

        # Add to completed downloads for display
        if result['success']:
            completed_downloads.append(result)

    active_downloads[session_id]['status'] = 'completed'
    active_downloads[session_id]['progress'] = 100
    active_downloads[session_id]['results'] = results

    # Keep only the last 10 completed downloads in the list
    if len(completed_downloads) > 10:
        completed_downloads = completed_downloads[-10:]


@app.route('/')
def index():
    return render_template('index.html', active_downloads=active_downloads, completed_downloads=completed_downloads)


@app.route('/download', methods=['POST'])
def download():
    if 'url' in request.form and request.form['url'].strip():
        # Single URL download
        url = request.form['url'].strip()
        session_id = str(uuid.uuid4())

        active_downloads[session_id] = {
            'type': 'single',
            'urls': [url],
            'status': 'starting',
            'progress': 0,
            'current_url': url
        }

        thread = threading.Thread(
            target=process_url_list, args=([url], session_id))
        thread.daemon = True
        thread.start()

        flash('Download started!', 'success')

    elif 'url_file' in request.files and request.files['url_file'].filename:
        # File upload with multiple URLs
        file = request.files['url_file']
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path)

        with open(temp_path, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]

        if urls:
            session_id = str(uuid.uuid4())
            active_downloads[session_id] = {
                'type': 'batch',
                'urls': urls,
                'status': 'starting',
                'progress': 0,
                'current_url': ''
            }

            thread = threading.Thread(
                target=process_url_list, args=(urls, session_id))
            thread.daemon = True
            thread.start()

            flash(f'Batch download started with {len(urls)} URLs!', 'success')
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
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok Video Downloader</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding-top: 20px; }
        .download-card { margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12 text-center mb-4">
                <h1>📥 TikTok Video Downloader</h1>
                <p class="lead">Download single or multiple TikTok videos</p>
            </div>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📹 Single Video Download</h5>
                    </div>
                    <div class="card-body">
                        <form action="/download" method="post">
                            <div class="mb-3">
                                <label for="url" class="form-label">TikTok URL</label>
                                <input type="url" class="form-control" id="url" name="url" placeholder="https://www.tiktok.com/@user/video/1234567890" required>
                            </div>
                            <button type="submit" class="btn btn-primary">Download</button>
                        </form>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>📋 Batch Download</h5>
                    </div>
                    <div class="card-body">
                        <form action="/download" method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label for="url_file" class="form-label">Upload URL List File</label>
                                <input type="file" class="form-control" id="url_file" name="url_file" accept=".txt">
                                <div class="form-text">Text file with one URL per line</div>
                            </div>
                            <button type="submit" class="btn btn-primary">Upload & Download</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-12">
                <h3>🔄 Active Downloads</h3>
                {% for id, download in active_downloads.items() %}
                {% if download.status != 'completed' %}
                <div class="card download-card">
                    <div class="card-body">
                        <h5 class="card-title">{{ download.type|capitalize }} Download</h5>
                        <p>Status: {{ download.status|capitalize }}</p>
                        <p>Current URL: {{ download.current_url }}</p>
                        <div class="progress">
                            <div class="progress-bar" role="progressbar" style="width: {{ download.progress }}%" 
                                 aria-valuenow="{{ download.progress }}" aria-valuemin="0" aria-valuemax="100">
                                {{ download.progress }}%
                            </div>
                        </div>
                    </div>
                </div>
                {% endif %}
                {% endfor %}
                
                <h3>✅ Completed Downloads</h3>
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>URL</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for download in completed_downloads %}
                            <tr>
                                <td>{{ download.title }}</td>
                                <td><a href="{{ download.url }}" target="_blank">{{ download.url[:30] }}...</a></td>
                                <td><a href="/downloads/{{ download.filename }}" class="btn btn-sm btn-success">Download</a></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Auto-refresh the page every 5 seconds to update download status
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("🌐 Starting Flask Web UI for TikTok Downloader")
    app.run(debug=True, host='0.0.0.0', port=5000)
