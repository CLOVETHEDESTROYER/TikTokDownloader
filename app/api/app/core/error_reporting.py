import logging
from typing import Optional, Dict, Any
from datetime import datetime
from .metrics import DOWNLOAD_ERRORS
from .logging_config import logger


class ErrorReporter:
    @staticmethod
    def report_error(
        error_type: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        platform: Optional[str] = None,
        url: Optional[str] = None
    ) -> None:
        """
        Comprehensive error reporting that includes:
        - Structured logging with context
        - Metric tracking
        - Request tracing
        """
        error_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": error_type,
            "message": message,
            "context": context or {},
            "user_id": user_id,
            "request_id": request_id,
            "platform": platform,
            "url": url
        }

        # Log the error with full context
        logger.error(
            f"Error occurred: {message}",
            extra={
                "error_data": error_data,
                "traceback": True  # Enable traceback logging
            }
        )

        # Update error metrics
        if platform:
            DOWNLOAD_ERRORS.labels(
                platform=platform,
                error_type=error_type
            ).inc()

    @staticmethod
    def report_download_error(
        error: Exception,
        platform: str,
        url: str,
        session_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Specialized method for reporting download-related errors
        with pre-filled download context
        """
        error_context = {
            "session_id": session_id,
            "url": url,
            "platform": platform,
            **(context or {})
        }

        ErrorReporter.report_error(
            error_type=type(error).__name__,
            message=str(error),
            context=error_context,
            request_id=session_id,
            platform=platform,
            url=url
        )

    @staticmethod
    def report_validation_error(
        error: Exception,
        data: Dict[str, Any],
        request_id: Optional[str] = None
    ) -> None:
        """
        Specialized method for reporting validation errors
        with the invalid data context
        """
        error_context = {
            "validation_data": data,
            "validation_errors": str(error)
        }

        ErrorReporter.report_error(
            error_type="ValidationError",
            message=f"Validation error: {str(error)}",
            context=error_context,
            request_id=request_id
        )
