from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer, String, Text

from app.db.base import Base


class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    UNDER_AI_REVIEW = "UNDER_AI_REVIEW"
    UNDER_RECRUITER_REVIEW = "UNDER_RECRUITER_REVIEW"
    INTERVIEW = "INTERVIEW"
    OFFER = "OFFER"
    REJECTED = "REJECTED"
    HOLD = "HOLD"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume = Column(String(500), nullable=True)
    cover_letter = Column(Text, nullable=True)
    status = Column(
        SqlEnum(ApplicationStatus),
        nullable=False,
        default=ApplicationStatus.APPLIED,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
