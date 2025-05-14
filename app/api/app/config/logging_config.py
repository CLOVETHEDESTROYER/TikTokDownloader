import os
import logging.config
from .settings import LOG_FOLDER

# Ensure log directory exists
os.makedirs(LOG_FOLDER, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_FOLDER, 'tiktok_service.log'),
            'mode': 'a',
            'formatter': 'detailed',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'app.services.tiktok': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

def setup_logging():
    """Initialize logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG) 