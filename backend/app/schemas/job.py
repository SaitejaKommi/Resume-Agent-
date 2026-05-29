from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    filename: str | None
    jd_text: str
    extracted_skills: list[str]
    created_at: datetime


class JobUploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    job_id: int


class JobListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[JobRead]
