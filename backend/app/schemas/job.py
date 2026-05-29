from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    user_id: int
    jd_text: str


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    jd_text: str
    extracted_skills: list[str]
    created_at: datetime
