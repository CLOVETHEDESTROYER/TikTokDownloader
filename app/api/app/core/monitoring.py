from prometheus_client import Counter, Histogram, Gauge
from typing import Dict, Any
import time
import psutil
from .logging_config import logger

# Download metrics
download_requests_total = Counter(
    'download_requests_total',
    'Total number of download requests',
    ['platform', 'status']  # Labels for different platforms and success/failure
)

download_duration_seconds = Histogram(
    'download_duration_seconds',
    'Time spent downloading videos',
    ['platform'],
    # Custom buckets in seconds
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

active_downloads = Gauge(
    'active_downloads',
    'Number of currently active downloads'
)

# Rate limiting metrics
rate_limit_hits = Counter(
    'rate_limit_hits_total',
    'Total number of rate limit hits',
    ['endpoint']
)

# Error metrics
error_counter = Counter(
    'errors_total',
    'Total number of errors',
    ['type']
)

# System metrics
system_memory_usage = Gauge(
    'system_memory_usage_bytes',
    'Current system memory usage in bytes'
)

system_cpu_usage = Gauge(
    'system_cpu_usage_percent',
    'Current system CPU usage percentage'
)

disk_usage = Gauge(
    'disk_usage_bytes',
    'Current disk usage in bytes',
    ['mount_point']
)


class MetricsCollector:
    @staticmethod
    def record_download_attempt(platform: str, status: str) -> None:
        """Record a download attempt"""
        download_requests_total.labels(platform=platform, status=status).inc()
        logger.info(f"Download attempt recorded", extra={
            "platform": platform,
            "status": status,
            "metric": "download_requests_total"
        })

    @staticmethod
    def track_download_duration(platform: str) -> None:
        """Context manager to track download duration"""
        return download_duration_seconds.labels(platform=platform).time()

    @staticmethod
    def update_active_downloads(count: int) -> None:
        """Update the number of active downloads"""
        active_downloads.set(count)

    @staticmethod
    def record_rate_limit_hit(endpoint: str) -> None:
        """Record a rate limit hit"""
        rate_limit_hits.labels(endpoint=endpoint).inc()
        rate_limit_logger.warning(f"Rate limit hit", extra={
            "endpoint": endpoint,
            "metric": "rate_limit_hits"
        })

    @staticmethod
    def record_error(error_type: str) -> None:
        """Record an error"""
        error_counter.labels(type=error_type).inc()
        logger.error(f"Error recorded", extra={
            "error_type": error_type,
            "metric": "errors_total"
        })

    @staticmethod
    def update_system_metrics() -> None:
        """Update system metrics"""
        try:
            # Memory usage
            memory = psutil.virtual_memory()
            system_memory_usage.set(memory.used)

            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            system_cpu_usage.set(cpu_percent)

            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage.labels(mount_point='/').set(disk.used)

            logger.info("System metrics updated", extra={
                "memory_used": memory.used,
                "cpu_percent": cpu_percent,
                "disk_used": disk.used
            })
        except Exception as e:
            logger.error(f"Error updating system metrics: {str(e)}")


# Example usage in a download function:
"""
async def download_video(url: str, platform: str):
    metrics = MetricsCollector()
    
    try:
        # Increment active downloads
        active_downloads.inc()
        
        # Track download duration
        with metrics.track_download_duration(platform):
            # Perform download
            result = await perform_download(url)
            
        # Record successful download
        metrics.record_download_attempt(platform, "success")
        
    except Exception as e:
        # Record error
        metrics.record_error(type(e).__name__)
        metrics.record_download_attempt(platform, "failure")
        raise
    finally:
        # Decrement active downloads
        active_downloads.dec()
"""
