from sqlalchemy.orm import Session

from app.model.job_model import Job, JobStatus
from app.schema.job_schema import JobCreate, JobUpdate


def create_job(db: Session, data: JobCreate, recruiter_id: int):
    job = Job(
        title=data.title,
        description=data.description,
        requirements=data.requirements,
        department=data.department,
        experience_required=data.experience_required,
        job_role=data.job_role,
        status=data.status,
        created_by=recruiter_id,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job_by_id(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def list_jobs(
    db: Session,
    search: str | None,
    department: str | None,
    status_filter: JobStatus | None,
    page: int,
    page_size: int,
):
    query = db.query(Job)

    if search:
        search_text = f"%{search}%"
        query = query.filter(
            (Job.title.ilike(search_text))
            | (Job.description.ilike(search_text))
            | (Job.requirements.ilike(search_text))
        )

    if department:
        query = query.filter(Job.department == department)

    if status_filter:
        query = query.filter(Job.status == status_filter)

    total = query.count()
    offset_value = (page - 1) * page_size
    jobs = (
        query.order_by(Job.created_at.desc())
        .offset(offset_value)
        .limit(page_size)
        .all()
    )

    return total, jobs


def update_job(db: Session, job: Job, data: JobUpdate):
    if data.title is not None:
        job.title = data.title
    if data.description is not None:
        job.description = data.description
    if data.requirements is not None:
        job.requirements = data.requirements
    if data.department is not None:
        job.department = data.department
    if data.experience_required is not None:
        job.experience_required = data.experience_required
    if data.job_role is not None:
        job.job_role = data.job_role
    if data.status is not None:
        job.status = data.status

    db.commit()
    db.refresh(job)
    return job


def close_job(db: Session, job: Job):
    job.status = JobStatus.CLOSED
    db.commit()
    db.refresh(job)
    return job
