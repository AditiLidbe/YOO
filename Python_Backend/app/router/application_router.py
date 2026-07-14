from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from typing import Optional

from app.db.base import get_db
from app.dependency.gateway_user import get_gateway_user
from app.model.application_model import ApplicationStatus
from app.schema.application_schema import ApplicationListResponse, ApplicationResponse, ApplicationStatusUpdate
from app.service import ai_service, application_service, s3_service


router = APIRouter(tags=["Module 2 - Applications"])


@router.post("/jobs/{job_id}/apply", response_model=ApplicationResponse)
def apply_to_job(
    job_id: int,
    background_tasks: BackgroundTasks,
    cover_letter: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_gateway_user),
):
    resume_path = s3_service.upload_resume(resume, current_user.id, job_id)
    application = application_service.apply_to_job(
        db,
        current_user,
        job_id,
        resume_path,
        cover_letter,
    )
    background_tasks.add_task(ai_service.screen_application, application.id)
    return application


@router.get("/candidates/me/applications", response_model=ApplicationListResponse)
def get_my_applications(
    status: Optional[ApplicationStatus] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_gateway_user),
):
    return application_service.list_candidate_applications(
        db,
        current_user,
        status,
        page,
        page_size,
    )


@router.get("/recruiters/me/applications", response_model=ApplicationListResponse)
def get_recruiter_applications(
    status: Optional[ApplicationStatus] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_gateway_user),
):
    return application_service.list_recruiter_applications(
        db,
        current_user,
        status,
        page,
        page_size,
    )


@router.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_gateway_user),
):
    return application_service.get_application_for_current_user(
        db,
        current_user,
        application_id,
    )


@router.get("/applications/{application_id}/resume-url")
def get_resume_url(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_gateway_user),
):
    application = application_service.get_application_for_current_user(
        db,
        current_user,
        application_id,
    )
    return {"download_url": s3_service.get_download_url(application.resume)}


@router.patch("/applications/{application_id}/status", response_model=ApplicationResponse)
def update_application_status(
    application_id: int,
    data: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_gateway_user),
):
    return application_service.update_application_status(
        db,
        current_user,
        application_id,
        data,
    )
