from sqlalchemy.orm import Session

from app.model.application_model import Application, ApplicationStatus
from app.model.job_model import Job
from app.schema.application_schema import ApplicationCreate, ApplicationStatusUpdate


def get_application_by_id(db: Session, application_id: int):
    return db.query(Application).filter(Application.id == application_id).first()


def get_application_by_candidate_and_job(
    db: Session,
    candidate_id: int,
    job_id: int,
):
    return (
        db.query(Application)
        .filter(
            Application.candidate_id == candidate_id,
            Application.job_id == job_id,
        )
        .first()
    )


def create_application(
    db: Session,
    candidate_id: int,
    job_id: int,
    data: ApplicationCreate,
):
    application = Application(
        candidate_id=candidate_id,
        job_id=job_id,
        resume=data.resume,
        cover_letter=data.cover_letter,
        status=ApplicationStatus.UNDER_AI_REVIEW,
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def list_candidate_applications(
    db: Session,
    candidate_id: int,
    status_filter: ApplicationStatus | None,
    page: int,
    page_size: int,
):
    query = db.query(Application).filter(Application.candidate_id == candidate_id)

    if status_filter:
        query = query.filter(Application.status == status_filter)

    total = query.count()
    offset_value = (page - 1) * page_size
    applications = (
        query.order_by(Application.created_at.desc())
        .offset(offset_value)
        .limit(page_size)
        .all()
    )

    return total, applications


def list_recruiter_applications(
    db: Session,
    recruiter_id: int,
    status_filter: ApplicationStatus | None,
    page: int,
    page_size: int,
):
    query = (
        db.query(Application)
        .join(Job, Application.job_id == Job.id)
        .filter(Job.created_by == recruiter_id)
    )

    if status_filter:
        query = query.filter(Application.status == status_filter)

    total = query.count()
    offset_value = (page - 1) * page_size
    applications = (
        query.order_by(Application.created_at.desc())
        .offset(offset_value)
        .limit(page_size)
        .all()
    )

    return total, applications


def update_application_status(
    db: Session,
    application: Application,
    data: ApplicationStatusUpdate,
):
    application.status = data.status
    db.commit()
    db.refresh(application)
    return application
