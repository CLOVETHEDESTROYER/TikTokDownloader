from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import DownloaderException
from typing import Union, Dict, Any
import sys
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def downloader_exception_handler(
    request: Request,
    exc: DownloaderException
) -> JSONResponse:
    """Handle custom downloader exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "type": exc.__class__.__name__,
            **exc.extra
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: Union[ValueError, TypeError]
) -> JSONResponse:
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "detail": str(exc),
            "type": "ValidationError"
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected errors"""
    # Log the full error with traceback
    error_details = {
        "error": str(exc),
        "type": exc.__class__.__name__,
        "traceback": traceback.format_exception(*sys.exc_info())
    }

    logger.error(
        f"Unexpected error processing request to {request.url}",
        extra=error_details
    )

    # Return a sanitized response to the client
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred",
            "type": "InternalServerError",
            "request_id": request.state.request_id if hasattr(request.state, 'request_id') else None
        }
    )


def setup_error_handlers(app: Any) -> None:
    """Configure error handlers for the application"""
    app.add_exception_handler(
        DownloaderException, downloader_exception_handler)
    app.add_exception_handler(ValueError, validation_exception_handler)
    app.add_exception_handler(TypeError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
