from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
import uvicorn
import os
import uuid
from .api.routes import downloads
from .core.error_handlers import setup_error_handlers
from .core.config import settings
from . import routes_test
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import logging
import time
import json
from .core.logging_config import setup_logging
from .core.exceptions import DownloaderException
from pydantic import BaseModel
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge
from .routes import tiktok as tiktok_routes

# Load environment variables
load_dotenv()

# Override settings for development
if os.getenv("ENV", "development") == "development":
    os.environ["REQUIRE_API_KEY"] = "false"

# Set up logging
setup_logging()
logger = logging.getLogger("app")

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize API key security
api_key_header = APIKeyHeader(
    name=settings.API_KEY_HEADER_NAME, auto_error=False)

# Create metrics
REQUEST_COUNT = Counter(
    'request_count', 'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'request_latency_seconds', 'Request latency',
    ['app_name', 'endpoint']
)
ACTIVE_CONNECTIONS = Gauge(
    'active_connections', 'Active connections',
    ['app_name']
)


@asynccontextmanager
async def lifespan(app):
    # Startup logic (if any)
    yield
    # Shutdown logic (if any)

app = FastAPI(
    title="Social Media Downloader API",
    description="API for downloading TikTok and Instagram content",
    version="1.0.0",
    lifespan=lifespan
)

# Debug log the configuration
logger.info(f"Starting application in {settings.ENV} mode")
logger.info(f"CORS ALLOW METHODS: {settings.CORS_ALLOW_METHODS}")
logger.info(f"CORS ALLOW HEADERS: {settings.CORS_ALLOW_HEADERS}")
logger.info(f"FRONTEND URL: {settings.FRONTEND_URL}")
logger.info(f"ALLOWED ORIGINS: {settings.ALLOWED_ORIGINS}")
logger.info(f"API KEY REQUIRED: {settings.REQUIRE_API_KEY}")

# Add rate limiter to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    expose_headers=settings.CORS_EXPOSE_HEADERS,
    max_age=settings.CORS_MAX_AGE,
)

# Create downloads directory if it doesn't exist
os.makedirs(settings.DOWNLOAD_FOLDER, exist_ok=True)

# Mount the downloads directory as a static file directory
app.mount("/downloads",
          StaticFiles(directory=settings.DOWNLOAD_FOLDER), name="downloads")

# Setup error handlers
setup_error_handlers(app)

# API Key dependency for admin-only endpoints


async def verify_admin_api_key(api_key: str = Depends(api_key_header)):
    if settings.ADMIN_API_KEY and api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin API key",
        )
    return api_key

# API Key dependency for general endpoints


async def verify_api_key(api_key: str = Depends(api_key_header)):
    # Skip API key check in development mode if configured
    if settings.ENV == "development" and not settings.REQUIRE_API_KEY:
        return api_key

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Check if the API key matches either the admin key or the website key
    if (settings.ADMIN_API_KEY and api_key == settings.ADMIN_API_KEY) or \
       (settings.WEBSITE_API_KEY and api_key == settings.WEBSITE_API_KEY):
        return api_key

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API key",
        headers={"WWW-Authenticate": "ApiKey"},
    )

# Request ID middleware


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response

# Path patterns that don't require API key verification
OPEN_API_PATHS = [
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
]

# API Key middleware


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    # Skip authentication for OPTIONS requests (CORS preflight)
    if request.method == "OPTIONS":
        return await call_next(request)

    # Skip authentication for open paths
    for path in OPEN_API_PATHS:
        if request.url.path.startswith(path):
            return await call_next(request)

    # Skip API key check in development mode if configured
    if settings.ENV == "development" and not settings.REQUIRE_API_KEY:
        return await call_next(request)

    # Check API key
    api_key = request.headers.get(settings.API_KEY_HEADER_NAME)

    # If no API key is provided and it's required
    if not api_key and settings.REQUIRE_API_KEY:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "API key is missing"},
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # If API key is provided, validate it
    if api_key and settings.REQUIRE_API_KEY:
        if (settings.ADMIN_API_KEY and api_key == settings.ADMIN_API_KEY) or \
           (settings.WEBSITE_API_KEY and api_key == settings.WEBSITE_API_KEY):
            return await call_next(request)

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Invalid API key"},
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return await call_next(request)

# Health check endpoint


@app.get("/health")
@limiter.limit("60/minute")
async def health_check(request: Request):
    return {
        "status": "ok",
        "version": app.version,
        "env": settings.ENV
    }

# Include our download routes
app.include_router(downloads.router, prefix="/api/v1", tags=["downloads"])

# Include TikTok routes from app/routes
app.include_router(tiktok_routes.router, tags=["tiktok"])

# Include our test routes for debugging only
if settings.DEBUG:
    app.include_router(routes_test.router, prefix="/test", tags=["test"])


@app.get("/")
@limiter.limit("60/minute")
async def root(request: Request):
    return {
        "message": "Welcome to Social Media Downloader API",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "env": settings.ENV
    }


@app.get("/metrics")
async def metrics(api_key: str = Depends(verify_admin_api_key)):
    """Endpoint for Prometheus metrics - admin access only"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Middleware for request ID and timing


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Track metrics
        ACTIVE_CONNECTIONS.labels(app_name="tiktok_downloader").inc()
        start_time = time.time()

        try:
            response = await call_next(request)

            # Record metrics
            process_time = time.time() - start_time
            REQUEST_LATENCY.labels(
                app_name="tiktok_downloader",
                endpoint=request.url.path
            ).observe(process_time)

            REQUEST_COUNT.labels(
                app_name="tiktok_downloader",
                method=request.method,
                endpoint=request.url.path,
                http_status=response.status_code
            ).inc()

            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            logger.error(f"Error occurred: {exc}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
        finally:
            ACTIVE_CONNECTIONS.labels(app_name="tiktok_downloader").dec()

# Exception handler for custom exceptions


@app.exception_handler(DownloaderException)
async def downloader_exception_handler(request: Request, exc: DownloaderException):
    logger.error(f"Error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Exception handler for generic exceptions


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"},
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS
    )
