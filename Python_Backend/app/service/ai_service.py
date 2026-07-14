import requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import Session as DBSession
from app.model.ai_model import AIRecommendation, AICheckType
from app.model.application_model import ApplicationStatus
from app.repository import ai_repository, application_repository, job_repository
from app.utils.config import setting


def get_ai_comment(prompt: str):
    if not setting.OPENAI_API_KEY:
        return "AI comment skipped."

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {setting.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": setting.OPENAI_MODEL,
            "input": prompt,
        },
    )

    if response.status_code != 200:
        return "AI comment failed."

    data = response.json()
    return data.get("output_text", "No AI comment.")


def check_skill(job, application):
    prompt = (
        "Give a short comment about skill match. "
        f"Job requirements: {job.requirements}. "
        f"Resume: {application.resume}. "
        f"Cover letter: {application.cover_letter}."
    )

    comment = get_ai_comment(prompt)
    score = 40
    if application.resume:
        score = 60
    if application.cover_letter:
        score = 70

    return score, comment


def check_experience(job, candidate):
    prompt = (
        "Give a short comment about experience fit. "
        f"Required experience: {job.experience_required}. "
        f"Candidate experience: {candidate.work_experience}."
    )

    comment = get_ai_comment(prompt)
    required = job.experience_required or 0
    actual = candidate.work_experience or 0

    if required == 0:
        score = 70
    elif actual >= required:
        score = 85
    else:
        score = 45

    return score, comment


def check_cover_letter(job, application):
    if not application.cover_letter:
        return 20, "Cover letter is missing."

    prompt = (
        "Give a short comment about this cover letter. "
        f"Job title: {job.title}. "
        f"Cover letter: {application.cover_letter}."
    )

    comment = get_ai_comment(prompt)
    return 70, comment


def check_completeness(application, candidate):
    prompt = (
        "Give a short comment about application completeness. "
        f"Resume: {application.resume}. "
        f"Cover letter: {application.cover_letter}. "
        f"Education: {candidate.highest_education}. "
        f"Experience: {candidate.work_experience}."
    )

    comment = get_ai_comment(prompt)
    score = 0

    if application.resume:
        score = score + 40
    if application.cover_letter:
        score = score + 20
    if candidate.highest_education:
        score = score + 20
    if candidate.work_experience is not None:
        score = score + 20

    return score, comment


def get_recommendation(score: int):
    if score >= 75:
        return AIRecommendation.STRONG_FIT
    if score >= 50:
        return AIRecommendation.POSSIBLE_FIT
    return AIRecommendation.NOT_FIT


def screen_application(application_id: int):
    db = DBSession()

    try:
        application = application_repository.get_application_by_id(db, application_id)
        if application is None:
            return

        job = job_repository.get_job_by_id(db, application.job_id)
        candidate = ai_repository.get_candidate_by_id(db, application.candidate_id)
        if job is None or candidate is None:
            return

        ai = ai_repository.get_ai_by_application_id(db, application_id)
        if ai is None:
            ai = ai_repository.create_ai(db, application_id)

        skill_score, skill_comment = check_skill(job, application)
        experience_score, experience_comment = check_experience(job, candidate)
        letter_score, letter_comment = check_cover_letter(job, application)
        complete_score, complete_comment = check_completeness(application, candidate)

        ai_repository.create_ai_result(
            db, ai.id, AICheckType.SKILL, skill_score, skill_comment
        )
        ai_repository.create_ai_result(
            db, ai.id, AICheckType.EXPERIENCE, experience_score, experience_comment
        )
        ai_repository.create_ai_result(
            db, ai.id, AICheckType.COVER_LETTER, letter_score, letter_comment
        )
        ai_repository.create_ai_result(
            db, ai.id, AICheckType.COMPLETENESS, complete_score, complete_comment
        )

        total = skill_score + experience_score + letter_score + complete_score
        average = int(total / 4)
        recommendation = get_recommendation(average)
        summary = f"Average score: {average}. Final result: {recommendation.value}."

        ai_repository.complete_ai(db, ai, summary, recommendation)
        ai_repository.update_application_status(
            db, application, ApplicationStatus.UNDER_RECRUITER_REVIEW
        )
    except Exception as exc:
        ai = ai_repository.get_ai_by_application_id(db, application_id)
        if ai:
            ai_repository.fail_ai(db, ai, f"AI screening failed: {exc}")
    finally:
        db.close()


def get_ai_for_application(db: Session, application_id: int):
    ai = ai_repository.get_ai_by_application_id(db, application_id)
    if ai is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI result not found",
        )

    ai.results = ai_repository.get_ai_results(db, ai.id)
    return ai
