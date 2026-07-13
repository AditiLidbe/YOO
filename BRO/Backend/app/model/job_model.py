from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer, String, Text

from app.db.base import Base


class JobStatus(str, Enum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    department = Column(String(150), nullable=False)
    experience_required = Column(Integer, nullable=True)
    job_role = Column(String(150), nullable=True)
    status = Column(SqlEnum(JobStatus), nullable=False, default=JobStatus.DRAFT)
    created_by = Column(Integer, ForeignKey("recruiters.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
