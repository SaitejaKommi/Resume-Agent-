from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    user_id: int
    resume_id: int
    job_id: int
    pdf_path: str | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    resume_id: int
    job_id: int
    ats_score: float
    pdf_path: str | None
    created_at: datetime
