from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Boolean, Column, Date, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CANDIDATE = "CANDIDATE"
    RECRUITER = "RECRUITER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(SqlEnum(UserRole), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    candidate = relationship(
        "Candidate",
        back_populates="user",
        uselist=False,
    )
    recruiter = relationship(
        "Recruiter",
        back_populates="user",
        uselist=False,
    )


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    highest_education = Column(String(150), nullable=True)
    marks_scored = Column(String(50), nullable=True)
    year_of_passing = Column(Date, nullable=True)
    cover_letter = Column(Text, nullable=True)
    work_experience = Column(Integer, nullable=True)
    profile_photo = Column(String(500), nullable=True)
    resume = Column(String(500), nullable=True)

    user = relationship("User", back_populates="candidate")


class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    company_name = Column(String(255), nullable=True)
    company_description = Column(Text, nullable=True)

    user = relationship("User", back_populates="recruiter")
