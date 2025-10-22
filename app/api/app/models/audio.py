from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class AudioExtractRequest(BaseModel):
    url: HttpUrl


class AudioBatchExtractRequest(BaseModel):
    urls: List[HttpUrl]


class AudioExtractResponse(BaseModel):
    session_id: str
    status: str
    message: str
    audio_url: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[float] = None
    platform: Optional[str] = None
