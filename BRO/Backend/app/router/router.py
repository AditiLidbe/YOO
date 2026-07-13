from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.dependencies.RBAC.role_checker import role_necessary
from app.dependencies.jwt.handler import get_current_user
from app.model.user_model import User, UserRole
from app.schema.user_schema import (
    AdminUserCreate,
    CandidateProfileResponse,
    CandidateProfileUpdate,
    OTPRequest,
    OTPVerify,
    RefreshTokenRequest,
    RecruiterProfileResponse,
    RecruiterProfileUpdate,
    Token,
    UserResponse,
)
from app.service.auth_service import (
    refresh_access_token,
    request_login_otp,
    verify_login_otp,
)
from app.service.user_service import (
    create_user_by_admin,
    update_candidate_profile,
    update_recruiter_profile,
)


router = APIRouter(tags=["Module 1 - Accounts and Access"])


@router.post("/admin/bootstrap", response_model=UserResponse)
def bootstrap_first_admin(data: AdminUserCreate, db: Session = Depends(get_db)):
    if data.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bootstrap user must be ADMIN",
        )

    has_users = db.query(User).first()
    if has_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bootstrap is allowed only before the first user is created",
        )

    return create_user_by_admin(data, db)


@router.post(
    "/admin/users",
    response_model=UserResponse,
    dependencies=[Depends(role_necessary(UserRole.ADMIN.value))],
)
def create_user(
    data: AdminUserCreate,
    db: Session = Depends(get_db),
):
    return create_user_by_admin(data, db)


@router.post("/auth/request-otp")
def request_otp(data: OTPRequest):
    return request_login_otp(data.email)


@router.post("/auth/verify-otp", response_model=Token)
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    return verify_login_otp(data.email, data.otp, db)


@router.post("/auth/refresh", response_model=Token)
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return refresh_access_token(data.refresh_token, db)


@router.get("/users/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.put("/candidates/me/profile", response_model=CandidateProfileResponse)
def update_my_candidate_profile(
    data: CandidateProfileUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_candidate_profile(db, current_user, data)


@router.put("/recruiters/me/profile", response_model=RecruiterProfileResponse)
def update_my_recruiter_profile(
    data: RecruiterProfileUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_recruiter_profile(db, current_user, data)
