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

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize API key security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

app = FastAPI(
    title="Social Media Downloader API",
    description="API for downloading TikTok and Instagram content",
    version="1.0.0"
)

# Add rate limiter to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization",
                   "X-Request-ID", "X-API-Key"],
    expose_headers=["X-Request-ID"],
    max_age=86400,
)

# Create downloads directory if it doesn't exist
os.makedirs(settings.DOWNLOAD_FOLDER, exist_ok=True)

# Mount the downloads directory as a static file directory
app.mount("/downloads",
          StaticFiles(directory=settings.DOWNLOAD_FOLDER), name="downloads")

# Setup error handlers
setup_error_handlers(app)

# API Key dependency for admin-only endpoints


async def verify_api_key(api_key: str = Depends(api_key_header)):
    if settings.ADMIN_API_KEY and api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return api_key

# Request ID middleware


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response

# Health check endpoint


@app.get("/health")
@limiter.limit("60/minute")
async def health_check(request: Request):
    return {
        "status": "healthy",
        "version": app.version,
        "env": settings.ENV
    }

# Include our download routes
app.include_router(downloads.router, prefix="/api/v1", tags=["downloads"])

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

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS
    )
