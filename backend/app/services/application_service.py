from sqlalchemy.orm import Session

from ai.ats_scoring import score_resume_against_job
from app.models.application import Application
from app.models.job import Job
from app.models.resume import Resume


def create_application(session: Session, user_id: int, resume_id: int, job_id: int, pdf_path: str | None = None) -> Application:
    resume = session.get(Resume, resume_id)
    job = session.get(Job, job_id)
    if resume is None or job is None:
        raise ValueError("Resume or job not found")

    score = score_resume_against_job(resume.raw_text, job.extracted_skills or [])
    application = Application(
        user_id=user_id,
        resume_id=resume_id,
        job_id=job_id,
        ats_score=score,
        pdf_path=pdf_path,
    )
    session.add(application)
    session.commit()
    session.refresh(application)
    return application
