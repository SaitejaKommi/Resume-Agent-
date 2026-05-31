from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResumeVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    master_profile_id: int
    application_id: int | None
    parent_version_id: int | None
    version_name: str
    target_role: str | None
    resume_text: str
    resume_content_json: dict = Field(default_factory=dict)
    ats_score: float
    ats_report_json: dict = Field(default_factory=dict)
    created_at: datetime


class ResumeVersionListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ResumeVersionRead]
