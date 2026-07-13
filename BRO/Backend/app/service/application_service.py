from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.model.application_model import ApplicationStatus
from app.model.job_model import JobStatus
from app.model.user_model import User, UserRole
from app.repository import application_repository, job_repository
from app.schema.application_schema import ApplicationCreate, ApplicationStatusUpdate


def get_candidate_profile(user: User):
    if user.role != UserRole.CANDIDATE or user.candidate is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can perform this action",
        )
    return user.candidate


def get_recruiter_profile(user: User):
    if user.role != UserRole.RECRUITER or user.recruiter is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can perform this action",
        )
    return user.recruiter


def apply_to_job(db: Session, user: User, job_id: int, data: ApplicationCreate):
    candidate = get_candidate_profile(user)
    job = job_repository.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    if job.status != JobStatus.OPEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can apply only to open jobs",
        )

    existing_application = application_repository.get_application_by_candidate_and_job(
        db,
        candidate.id,
        job.id,
    )
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied to this job",
        )

    return application_repository.create_application(db, candidate.id, job.id, data)


def list_candidate_applications(
    db: Session,
    user: User,
    status_filter: ApplicationStatus | None,
    page: int,
    page_size: int,
):
    candidate = get_candidate_profile(user)
    total, applications = application_repository.list_candidate_applications(
        db,
        candidate.id,
        status_filter,
        page,
        page_size,
    )
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": applications,
    }


def list_recruiter_applications(
    db: Session,
    user: User,
    status_filter: ApplicationStatus | None,
    page: int,
    page_size: int,
):
    recruiter = get_recruiter_profile(user)
    total, applications = application_repository.list_recruiter_applications(
        db,
        recruiter.id,
        status_filter,
        page,
        page_size,
    )
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": applications,
    }


def get_application_or_404(db: Session, application_id: int):
    application = application_repository.get_application_by_id(db, application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    return application


def get_application_for_current_user(db: Session, user: User, application_id: int):
    application = get_application_or_404(db, application_id)

    if user.role == UserRole.CANDIDATE:
        candidate = get_candidate_profile(user)
        if application.candidate_id == candidate.id:
            return application

    if user.role == UserRole.RECRUITER:
        recruiter = get_recruiter_profile(user)
        job = job_repository.get_job_by_id(db, application.job_id)
        if job and job.created_by == recruiter.id:
            return application

    if user.role == UserRole.ADMIN:
        return application

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You cannot access this application",
    )


def update_application_status(
    db: Session,
    user: User,
    application_id: int,
    data: ApplicationStatusUpdate,
):
    recruiter = get_recruiter_profile(user)
    application = get_application_or_404(db, application_id)
    job = job_repository.get_job_by_id(db, application.job_id)

    if job is None or job.created_by != recruiter.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only applications for your jobs",
        )

    return application_repository.update_application_status(db, application, data)
