from fastapi import APIRouter
from typing import List
from ..models.audio import AudioExtractRequest, AudioBatchExtractRequest, AudioExtractResponse
from ..services.audio_extractor import AudioExtractorService

router = APIRouter(prefix="/api/v1/audio", tags=["audio"])


@router.post("/extract", response_model=AudioExtractResponse)
async def extract_audio(request: AudioExtractRequest):
    """Extract audio from any supported platform video URL"""
    service = AudioExtractorService()
    return await service.extract_audio(request.url)


@router.post("/batch-extract", response_model=List[AudioExtractResponse])
async def batch_extract_audio(request: AudioBatchExtractRequest):
    """Extract audio from multiple video URLs"""
    service = AudioExtractorService()
    return await service.batch_extract_audio(request.urls)
