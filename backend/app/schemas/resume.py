from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeCreate(BaseModel):
    raw_text: str
    filename: str | None = None


class ResumeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    filename: str | None
    raw_text: str
    json_data: dict
    created_at: datetime


class ResumeUploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resume_id: int


class ResumeListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[ResumeRead]
