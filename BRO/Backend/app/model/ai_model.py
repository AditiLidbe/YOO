from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer, String, Text

from app.db.base import Base


class AIStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AIRecommendation(str, Enum):
    STRONG_FIT = "STRONG_FIT"
    POSSIBLE_FIT = "POSSIBLE_FIT"
    NOT_FIT = "NOT_FIT"


class AICheckType(str, Enum):
    SKILL = "SKILL"
    EXPERIENCE = "EXPERIENCE"
    COVER_LETTER = "COVER_LETTER"
    COMPLETENESS = "COMPLETENESS"


class AI(Base):
    __tablename__ = "ai"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    summary = Column(Text, nullable=True)
    recommendation = Column(SqlEnum(AIRecommendation), nullable=True)
    status = Column(SqlEnum(AIStatus), nullable=False, default=AIStatus.PENDING)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class AIResult(Base):
    __tablename__ = "ai_results"

    id = Column(Integer, primary_key=True, index=True)
    ai_id = Column(Integer, ForeignKey("ai.id"), nullable=False)
    check_type = Column(SqlEnum(AICheckType), nullable=False)
    score = Column(Integer, nullable=False)
    comments = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
