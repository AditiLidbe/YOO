from sqlalchemy.orm import Session

from app.model.application_model import Application
from app.model.user_model import Candidate


def save_candidate_resume(db: Session, candidate: Candidate, file_path: str):
    candidate.resume = file_path
    db.commit()
    db.refresh(candidate)
    return candidate


def save_candidate_profile_photo(db: Session, candidate: Candidate, file_path: str):
    candidate.profile_photo = file_path
    db.commit()
    db.refresh(candidate)
    return candidate


def save_application_resume(
    db: Session,
    application: Application,
    file_path: str,
):
    application.resume = file_path
    db.commit()
    db.refresh(application)
    return application
