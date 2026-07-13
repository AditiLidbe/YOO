from sqlalchemy.orm import Session

from app.model.ai_model import AI, AIRecommendation, AIResult, AIStatus, AICheckType
from app.model.application_model import Application, ApplicationStatus
from app.model.user_model import Candidate


def create_ai(db: Session, application_id: int):
    ai = AI(application_id=application_id, status=AIStatus.PENDING)
    db.add(ai)
    db.commit()
    db.refresh(ai)
    return ai


def get_ai_by_application_id(db: Session, application_id: int):
    return db.query(AI).filter(AI.application_id == application_id).first()


def create_ai_result(
    db: Session,
    ai_id: int,
    check_type: AICheckType,
    score: int,
    comments: str,
):
    result = AIResult(
        ai_id=ai_id,
        check_type=check_type,
        score=score,
        comments=comments,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def get_ai_results(db: Session, ai_id: int):
    return db.query(AIResult).filter(AIResult.ai_id == ai_id).all()


def complete_ai(
    db: Session,
    ai: AI,
    summary: str,
    recommendation: AIRecommendation,
):
    ai.summary = summary
    ai.recommendation = recommendation
    ai.status = AIStatus.COMPLETED
    db.commit()
    db.refresh(ai)
    return ai


def fail_ai(db: Session, ai: AI, summary: str):
    ai.summary = summary
    ai.status = AIStatus.FAILED
    db.commit()
    db.refresh(ai)
    return ai


def update_application_status(
    db: Session,
    application: Application,
    status: ApplicationStatus,
):
    application.status = status
    db.commit()
    db.refresh(application)
    return application


def get_candidate_by_id(db: Session, candidate_id: int):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()
