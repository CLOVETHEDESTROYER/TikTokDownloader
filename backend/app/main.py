from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os
import uuid
from .api.routes import downloads
from .core.error_handlers import setup_error_handlers

app = FastAPI(
    title="Social Media Downloader API",
    description="API for downloading TikTok and Instagram content",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create downloads directory if it doesn't exist
os.makedirs("downloads", exist_ok=True)

# Mount the downloads directory as a static file directory
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

# Setup error handlers
setup_error_handlers(app)

# Request ID middleware


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response

# Health check endpoint


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": app.version
    }

# Include our download routes
app.include_router(downloads.router, prefix="/api/v1", tags=["downloads"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Social Media Downloader API",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
