from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.dependencies.jwt.handler import get_current_user
from app.model.user_model import UserRole
from app.repository import application_repository, file_repository, job_repository
from app.service import s3_service


router = APIRouter(prefix="/files", tags=["Files"])


def get_candidate(current_user):
    if current_user.role != UserRole.CANDIDATE or current_user.candidate is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can upload these files",
        )
    return current_user.candidate


@router.post("/upload")
def upload_files(
    application_id: int | None = Form(default=None),
    resume: UploadFile | None = File(default=None),
    profile_photo: UploadFile | None = File(default=None),
    application_resume: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    candidate = get_candidate(current_user)
    uploaded_files = {}

    if resume:
        folder = f"users/{current_user.id}/candidate/resume"
        file_path = s3_service.upload_file(resume, folder)
        file_repository.save_candidate_resume(db, candidate, file_path)
        uploaded_files["resume"] = file_path

    if profile_photo:
        folder = f"users/{current_user.id}/candidate/profile-photo"
        file_path = s3_service.upload_file(profile_photo, folder)
        file_repository.save_candidate_profile_photo(db, candidate, file_path)
        uploaded_files["profile_photo"] = file_path

    if application_resume:
        if application_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="application_id is required for application resume",
            )

        application = application_repository.get_application_by_id(db, application_id)
        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        if application.candidate_id != candidate.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can upload resume only for your own application",
            )

        folder = f"users/{current_user.id}/applications/{application_id}/resume"
        file_path = s3_service.upload_file(application_resume, folder)
        file_repository.save_application_resume(db, application, file_path)
        uploaded_files["application_resume"] = file_path

    if not uploaded_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Upload at least one file",
        )

    return {"uploaded_files": uploaded_files}


@router.get("/download")
def get_download_url(
    file_path: str,
    current_user=Depends(get_current_user),
):
    user_folder = f"users/{current_user.id}/"
    if not file_path.startswith(user_folder):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can access only your own files",
        )

    return {"download_url": s3_service.get_file_url(file_path)}


@router.get("/applications/{application_id}/resume")
def get_application_resume_url(
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

    if not application.resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not uploaded",
        )

    if current_user.role == UserRole.ADMIN:
        return {"download_url": s3_service.get_file_url(application.resume)}

    if current_user.role == UserRole.CANDIDATE and current_user.candidate:
        if application.candidate_id == current_user.candidate.id:
            return {"download_url": s3_service.get_file_url(application.resume)}

    if current_user.role == UserRole.RECRUITER and current_user.recruiter:
        job = job_repository.get_job_by_id(db, application.job_id)
        if job and job.created_by == current_user.recruiter.id:
            return {"download_url": s3_service.get_file_url(application.resume)}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You cannot access this resume",
    )
