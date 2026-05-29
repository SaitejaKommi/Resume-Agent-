from sqlalchemy.orm import Session

from ai.resume_analyzer import analyze_resume
from app.models.resume import Resume


def create_resume(session: Session, user_id: int, raw_text: str, json_data: dict | None = None) -> Resume:
    payload = json_data or analyze_resume(raw_text)
    resume = Resume(user_id=user_id, raw_text=raw_text, json_data=payload)
    session.add(resume)
    session.commit()
    session.refresh(resume)
    return resume
