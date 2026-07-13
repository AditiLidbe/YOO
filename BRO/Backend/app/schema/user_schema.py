from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.model.user_model import UserRole


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=4, max_length=8)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: UserRole


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    id: int
    email: EmailStr
    role: UserRole


class AdminUserCreate(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role: UserRole


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateProfileUpdate(BaseModel):
    highest_education: Optional[str] = None
    marks_scored: Optional[str] = None
    year_of_passing: Optional[date] = None
    cover_letter: Optional[str] = None
    work_experience: Optional[int] = Field(default=None, ge=0)
    profile_photo: Optional[str] = None
    resume: Optional[str] = None


class CandidateProfileResponse(CandidateProfileUpdate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class RecruiterProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None


class RecruiterProfileResponse(RecruiterProfileUpdate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
