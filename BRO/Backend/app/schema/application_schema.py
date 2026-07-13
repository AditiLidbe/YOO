from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.model.application_model import ApplicationStatus


class ApplicationCreate(BaseModel):
    resume: Optional[str] = None
    cover_letter: Optional[str] = None


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    resume: Optional[str]
    cover_letter: Optional[str]
    status: ApplicationStatus
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[ApplicationResponse]
