from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.dependencies.jwt.handler import get_current_user
from app.model.user_model import UserRole
from app.repository import application_repository, job_repository
from app.schema.ai_schema import AIResponse
from app.service import ai_service


router = APIRouter(prefix="/ai", tags=["Module 3 - AI"])


@router.get("/applications/{application_id}", response_model=AIResponse)
def get_ai_result(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    application = application_repository.get_application_by_id(db, application_id)
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if current_user.role == UserRole.ADMIN:
        return ai_service.get_ai_for_application(db, application_id)

    if current_user.role == UserRole.RECRUITER and current_user.recruiter:
        job = job_repository.get_job_by_id(db, application.job_id)
        if job and job.created_by == current_user.recruiter.id:
            return ai_service.get_ai_for_application(db, application_id)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Only the job recruiter can view AI result",
    )
