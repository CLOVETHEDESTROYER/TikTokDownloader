from prometheus_client import Counter, Histogram, Gauge

# Counter for total download requests
DOWNLOAD_REQUESTS = Counter(
    'download_requests_total',
    'Total number of download requests',
    ['platform', 'quality']
)

# Histogram for download duration
DOWNLOAD_DURATION = Histogram(
    'download_duration_seconds',
    'Time spent processing downloads',
    ['platform'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

# Gauge for current active downloads
ACTIVE_DOWNLOADS = Gauge(
    'active_downloads',
    'Number of downloads currently in progress',
    ['platform']
)

# Counter for download errors
DOWNLOAD_ERRORS = Counter(
    'download_errors_total',
    'Total number of failed downloads',
    ['platform', 'error_type']
)
