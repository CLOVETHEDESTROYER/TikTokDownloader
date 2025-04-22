from fastapi import APIRouter, HTTPException, WebSocket, Depends, BackgroundTasks, Request
from fastapi.responses import FileResponse
from ...models.download import (
    DownloadRequest,
    DownloadResponse,
    BatchDownloadRequest,
    BatchDownloadResponse,
    DownloadStatus
)
from ...services.download_manager import DownloadManager
from ..dependencies import check_rate_limit, check_download_limit, check_bulk_download_limit, get_quota
import asyncio
import os
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
download_manager = DownloadManager()

# Flag to track if cleanup task has been started
cleanup_task_started = False


async def ensure_cleanup_task_started():
    """Ensure the cleanup task is started if it hasn't been already."""
    global cleanup_task_started
    if not cleanup_task_started:
        await download_manager.start_cleanup_task()
        cleanup_task_started = True


@router.get("/quota")
async def get_remaining_quota(
    request: Request,
    quota: dict = Depends(get_quota)
):
    """Get the remaining quota for the current user."""
    limiter = request.app.state.limiter
    if limiter:
        limiter.limit("30/minute")(get_remaining_quota)(request)
    return quota


@router.post("/download", response_model=DownloadResponse)
async def create_download(
    request: Request,
    download_request: DownloadRequest,
    background_tasks: BackgroundTasks,
    _: None = Depends(check_rate_limit),
    __: None = Depends(check_download_limit)
) -> DownloadResponse:
    limiter = request.app.state.limiter
    if limiter:
        limiter.limit("10/minute")(create_download)(request)

    # Ensure cleanup task is started
    await ensure_cleanup_task_started()

    try:
        # Create a new download session
        session_id = await download_manager.create_download(
            url=str(download_request.url),
            platform=download_request.platform
        )

        # Process the download in the background
        background_tasks.add_task(
            download_manager.process_download,
            session_id,
            str(download_request.url),
            download_request.platform,
            download_request.quality
        )

        return DownloadResponse(
            session_id=session_id,
            status=DownloadStatus.PENDING,
            progress=0,
            url=download_request.url
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/batch-download", response_model=BatchDownloadResponse)
async def create_batch_download(
    request: Request,
    batch_request: BatchDownloadRequest,
    background_tasks: BackgroundTasks,
    _: None = Depends(check_rate_limit),
    __: None = Depends(check_bulk_download_limit)
) -> BatchDownloadResponse:
    limiter = request.app.state.limiter
    if limiter:
        limiter.limit("5/minute")(create_batch_download)(request)

    # Ensure cleanup task is started
    await ensure_cleanup_task_started()

    try:
        # Create a new download session
        session_id = await download_manager.create_download(
            url=str(batch_request.urls[0]),  # Use first URL for session
            platform=batch_request.platform
        )

        # Process the batch download in the background
        background_tasks.add_task(
            download_manager.process_batch_download,
            session_id,
            [str(url) for url in batch_request.urls],
            batch_request.platform,
            batch_request.quality
        )

        return BatchDownloadResponse(
            session_id=session_id,
            total_urls=len(batch_request.urls),
            status=DownloadStatus.PENDING,
            progress=0
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status/{session_id}", response_model=DownloadResponse)
async def get_download_status(
    request: Request,
    session_id: str,
    _: None = Depends(check_rate_limit)
) -> DownloadResponse:
    limiter = request.app.state.limiter
    if limiter:
        limiter.limit("60/minute")(get_download_status)(request)

    status = await download_manager.get_download_status(session_id)
    if status is None:
        raise HTTPException(
            status_code=404, detail="Download session not found")
    return status


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        # Ensure cleanup task is started
        await ensure_cleanup_task_started()

        while True:
            # Get the current status
            status = await download_manager.get_download_status(session_id)
            if status is None:
                await websocket.close(code=1000)
                break

            # Send the status to the client
            await websocket.send_json(status.dict())

            # If download is completed or failed, close the connection
            if status.status in [DownloadStatus.COMPLETED, DownloadStatus.FAILED]:
                await websocket.close(code=1000)
                break

            # Wait before sending the next update
            await asyncio.sleep(0.5)

    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        await websocket.close(code=1000)


@router.get("/file/{session_id}")
async def download_file(
    request: Request,
    session_id: str,
    _: None = Depends(check_rate_limit)
):
    """Download a video file directly."""
    limiter = request.app.state.limiter
    if limiter:
        limiter.limit("20/minute")(download_file)(request)

    # Ensure cleanup task is started
    await ensure_cleanup_task_started()

    try:
        # Get the download status
        status = await download_manager.get_download_status(session_id)
        if status is None:
            raise HTTPException(
                status_code=404,
                detail="Download session not found"
            )

        # Check if the download is completed
        if status.status != DownloadStatus.COMPLETED:
            raise HTTPException(
                status_code=400,
                detail=f"Download is not ready. Current status: {status.status}"
            )

        # Check if the file has expired
        if status.status == DownloadStatus.EXPIRED:
            raise HTTPException(
                status_code=410,
                detail="Download has expired. Please request a new download."
            )

        # Check if we have a filename
        if not status.filename:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        file_path = os.path.join(
            download_manager.download_folder, status.filename)

        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="File not found on server"
            )

        # Return the file with appropriate headers for download
        return FileResponse(
            path=file_path,
            filename=status.filename,
            media_type="video/mp4",
            headers={
                "Content-Disposition": f'attachment; filename="{status.filename}"'
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading file: {str(e)}"
        )
