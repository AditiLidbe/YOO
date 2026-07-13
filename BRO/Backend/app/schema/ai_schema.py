from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.model.ai_model import AIRecommendation, AIStatus, AICheckType


class AIResultResponse(BaseModel):
    id: int
    ai_id: int
    check_type: AICheckType
    score: int
    comments: str
    created_at: datetime

    class Config:
        from_attributes = True


class AIResponse(BaseModel):
    id: int
    application_id: int
    summary: Optional[str]
    recommendation: Optional[AIRecommendation]
    status: AIStatus
    created_at: datetime
    results: List[AIResultResponse] = []

    class Config:
        from_attributes = True
