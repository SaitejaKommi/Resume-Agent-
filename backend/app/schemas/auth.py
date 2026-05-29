from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime


class GitHubOAuthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPayload


class CurrentUserResponse(UserPayload):
    pass
