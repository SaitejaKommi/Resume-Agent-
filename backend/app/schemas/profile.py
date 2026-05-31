from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MasterProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    headline: str | None
    summary: str | None
    education_json: list = Field(default_factory=list)
    experience_json: list = Field(default_factory=list)
    skills_json: list = Field(default_factory=list)
    certifications_json: list = Field(default_factory=list)
    achievements_json: list = Field(default_factory=list)
    projects_json: list = Field(default_factory=list)
    github_json: dict = Field(default_factory=dict)
    portfolio_links_json: list = Field(default_factory=list)
    profile_completeness: int
    source_resume_id: int | None
    created_at: datetime
    updated_at: datetime


class MasterProfileUpdate(BaseModel):
    headline: str | None = None
    summary: str | None = None
    education_json: list | None = None
    experience_json: list | None = None
    skills_json: list | None = None
    certifications_json: list | None = None
    achievements_json: list | None = None
    projects_json: list | None = None
    github_json: dict | None = None
    portfolio_links_json: list | None = None
