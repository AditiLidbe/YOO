from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.model.user_model import Candidate, Recruiter, User, UserRole
from app.schema.user_schema import (
    AdminUserCreate,
    CandidateProfileUpdate,
    RecruiterProfileUpdate,
)
from app.service.email_service import send_actvation_link_email


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email.lower()).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user_by_admin(data: AdminUserCreate, db: Session):
    existing_user = get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    user = User(
        email=data.email.lower(),
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role,
        is_active=True,
    )
    db.add(user)
    db.flush()

    if data.role == UserRole.CANDIDATE:
        db.add(Candidate(user_id=user.id))
    elif data.role == UserRole.RECRUITER:
        db.add(Recruiter(user_id=user.id))

    db.commit()
    db.refresh(user)

    try:
        send_actvation_link_email(user.email, "Use login OTP to activate your account")
    except HTTPException as exc:
        print(f"Activation email was not sent: {exc.detail}")

    return user


def update_candidate_profile(db: Session, user: User, data: CandidateProfileUpdate):
    if user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can update candidate profile",
        )

    profile = user.candidate
    if profile is None:
        profile = Candidate(user_id=user.id)
        db.add(profile)
        db.flush()

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile


def update_recruiter_profile(db: Session, user: User, data: RecruiterProfileUpdate):
    if user.role != UserRole.RECRUITER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can update recruiter profile",
        )

    profile = user.recruiter
    if profile is None:
        profile = Recruiter(user_id=user.id)
        db.add(profile)
        db.flush()

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile
