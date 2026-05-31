from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApplicationCreate(BaseModel):
    resume_id: int
    job_id: int
    github_repos: list[str] = Field(default_factory=list)
    pdf_path: str | None = None
    company: str | None = None
    role_title: str | None = None
    status: str = "saved"
    date_applied: datetime | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    resume_id: int
    job_id: int
    company: str | None
    role_title: str | None
    status: str
    date_applied: datetime | None
    resume_version_id: int | None
    github_repos: list[str]
    ats_score: float
    pdf_path: str | None
    pipeline_result: dict
    created_at: datetime


class ApplicationListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ApplicationRead]


class ApplicationKanbanUpdate(BaseModel):
    kanban_status: str
