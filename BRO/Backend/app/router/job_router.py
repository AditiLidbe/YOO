from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.dependencies.jwt.handler import get_current_user
from app.model.job_model import JobStatus
from app.schema.job_schema import JobCreate, JobListResponse, JobResponse, JobUpdate
from app.service import job_service


router = APIRouter(prefix="/jobs", tags=["Module 2 - Jobs"])


@router.post("", response_model=JobResponse)
def create_job(
    data: JobCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return job_service.create_job(db, current_user, data)


@router.get("", response_model=JobListResponse)
def get_jobs(
    search: str | None = None,
    department: str | None = None,
    status: JobStatus | None = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
):
    return job_service.list_jobs(db, search, department, status, page, page_size)


@router.get("/open", response_model=JobListResponse)
def get_open_jobs(
    search: str | None = None,
    department: str | None = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
):
    return job_service.list_open_jobs(db, search, department, page, page_size)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    return job_service.get_job_or_404(db, job_id)


@router.patch("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    data: JobUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return job_service.update_job(db, current_user, job_id, data)


@router.delete("/{job_id}", response_model=JobResponse)
def close_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return job_service.close_job(db, current_user, job_id)
