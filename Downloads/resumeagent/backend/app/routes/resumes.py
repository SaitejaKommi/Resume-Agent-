from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeRead
from app.services.resume_service import create_resume

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post("", response_model=ResumeRead)
def create_resume_route(payload: ResumeCreate, db: Session = Depends(get_db)) -> ResumeRead:
    return create_resume(db, payload.user_id, payload.raw_text, payload.json_data)


@router.get("", response_model=list[ResumeRead])
def list_resumes(db: Session = Depends(get_db)) -> list[ResumeRead]:
    return db.query(Resume).order_by(Resume.created_at.desc()).all()


@router.get("/{resume_id}", response_model=ResumeRead)
def get_resume(resume_id: int, db: Session = Depends(get_db)) -> ResumeRead:
    resume = db.get(Resume, resume_id)
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume
