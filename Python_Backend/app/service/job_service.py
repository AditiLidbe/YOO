from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.model.job_model import JobStatus
from app.model.user_model import UserRole
from app.dependency.gateway_user import GatewayUser
from app.repository import job_repository
from app.schema.job_schema import JobCreate, JobUpdate


def get_recruiter_profile(db: Session, user: GatewayUser):
    if user.role != UserRole.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can perform this action",
        )
    recruiter = job_repository.get_recruiter_by_user_id(db, user.id)
    if recruiter is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recruiter profile not found",
        )
    return recruiter


def create_job(db: Session, user: GatewayUser, data: JobCreate):
    recruiter = get_recruiter_profile(db, user)
    return job_repository.create_job(db, data, recruiter.id)


def list_jobs(
    db: Session,
    search: Optional[str],
    department: Optional[str],
    status_filter: Optional[JobStatus],
    page: int,
    page_size: int,
):
    total, jobs = job_repository.list_jobs(
        db,
        search,
        department,
        status_filter,
        page,
        page_size,
    )
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": jobs,
    }


def list_open_jobs(
    db: Session,
    search: Optional[str],
    department: Optional[str],
    page: int,
    page_size: int,
):
    return list_jobs(
        db=db,
        search=search,
        department=department,
        status_filter=JobStatus.OPEN,
        page=page,
        page_size=page_size,
    )


def get_job_or_404(db: Session, job_id: int):
    job = job_repository.get_job_by_id(db, job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return job


def update_job(db: Session, user: GatewayUser, job_id: int, data: JobUpdate):
    recruiter = get_recruiter_profile(db, user)
    job = get_job_or_404(db, job_id)

    if job.created_by != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your own jobs",
        )

    return job_repository.update_job(db, job, data)


def close_job(db: Session, user: GatewayUser, job_id: int):
    recruiter = get_recruiter_profile(db, user)
    job = get_job_or_404(db, job_id)

    if job.created_by != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can close only your own jobs",
        )

    return job_repository.close_job(db, job)
