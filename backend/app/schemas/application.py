from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApplicationCreate(BaseModel):
    resume_id: int
    job_id: int
    github_repos: list[str] = Field(default_factory=list)
    pdf_path: str | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    resume_id: int
    job_id: int
    github_repos: list[str]
    ats_score: float
    pdf_path: str | None
    pipeline_result: dict
    created_at: datetime


class ApplicationListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ApplicationRead]
