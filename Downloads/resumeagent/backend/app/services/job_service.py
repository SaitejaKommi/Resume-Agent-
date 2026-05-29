from sqlalchemy.orm import Session

from ai.skill_extractor import extract_skills
from app.models.job import Job


def create_job(session: Session, user_id: int, jd_text: str) -> Job:
    job = Job(user_id=user_id, jd_text=jd_text, extracted_skills=extract_skills(jd_text))
    session.add(job)
    session.commit()
    session.refresh(job)
    return job
