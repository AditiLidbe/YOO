from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.model.job_model import JobStatus
from app.model.user_model import User, UserRole
from app.repository import job_repository
from app.schema.job_schema import JobCreate, JobUpdate


def get_recruiter_profile(user: User):
    if user.role != UserRole.RECRUITER or user.recruiter is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can perform this action",
        )
    return user.recruiter


def create_job(db: Session, user: User, data: JobCreate):
    recruiter = get_recruiter_profile(user)
    return job_repository.create_job(db, data, recruiter.id)


def list_jobs(
    db: Session,
    search: str | None,
    department: str | None,
    status_filter: JobStatus | None,
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
    search: str | None,
    department: str | None,
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


def update_job(db: Session, user: User, job_id: int, data: JobUpdate):
    recruiter = get_recruiter_profile(user)
    job = get_job_or_404(db, job_id)

    if job.created_by != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your own jobs",
        )

    return job_repository.update_job(db, job, data)


def close_job(db: Session, user: User, job_id: int):
    recruiter = get_recruiter_profile(user)
    job = get_job_or_404(db, job_id)

    if job.created_by != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can close only your own jobs",
        )

    return job_repository.close_job(db, job)
