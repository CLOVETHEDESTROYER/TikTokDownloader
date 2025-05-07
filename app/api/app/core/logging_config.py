import os
import logging.config
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if they exist
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging() -> None:
    """Configure logging for the application"""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JSONFormatter
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stdout"
            },
            "file_info": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": "logs/info.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": "INFO"
            },
            "file_error": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": "logs/error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": "ERROR"
            },
            "file_download": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": "logs/downloads.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": "INFO"
            },
            "file_rate_limit": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": "logs/rate_limits.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": "INFO"
            }
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file_info", "file_error"],
                "level": "INFO",
                "propagate": False
            },
            "app.downloads": {
                "handlers": ["file_download"],
                "level": "INFO",
                "propagate": True
            },
            "app.rate_limits": {
                "handlers": ["file_rate_limit"],
                "level": "INFO",
                "propagate": True
            }
        }
    }

    logging.config.dictConfig(logging_config)


# Create logger instances
logger = logging.getLogger("app")
download_logger = logging.getLogger("app.downloads")
rate_limit_logger = logging.getLogger("app.rate_limits")
