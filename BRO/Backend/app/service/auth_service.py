from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.caching.otp_service import generate_otp, save_otp, verify_otp
from app.dependencies.jwt.bearer import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.service.email_service import send_otp_email
from app.service.user_service import get_user_by_email, get_user_by_id


def request_login_otp(email: str):
    otp = generate_otp()
    save_otp(email, otp)
    send_otp_email(email, otp)
    return {"message": "OTP sent to email"}


def verify_login_otp(email: str, otp: str, db: Session):
    if not verify_otp(email, otp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP",
        )

    user = get_user_by_email(db, email)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    token_data = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role.value if hasattr(user.role, "value") else user.role,
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": token_data["role"],
    }


def refresh_access_token(refresh_token: str, db: Session):
    token_data = verify_token(refresh_token, expected_token_type="refresh")
    user = get_user_by_id(db, token_data.id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    data = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role.value if hasattr(user.role, "value") else user.role,
    }
    return {
        "access_token": create_access_token(data),
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": data["role"],
    }
