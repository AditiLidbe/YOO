from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.model.job_model import JobStatus


class JobCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    requirements: str = Field(min_length=1)
    department: str = Field(min_length=1, max_length=150)
    experience_required: Optional[int] = Field(default=None, ge=0)
    job_role: Optional[str] = Field(default=None, max_length=150)
    status: JobStatus = JobStatus.OPEN


class JobUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    requirements: Optional[str] = None
    department: Optional[str] = Field(default=None, max_length=150)
    experience_required: Optional[int] = Field(default=None, ge=0)
    job_role: Optional[str] = Field(default=None, max_length=150)
    status: Optional[JobStatus] = None


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    requirements: str
    department: str
    experience_required: Optional[int]
    job_role: Optional[str]
    status: JobStatus
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[JobResponse]
