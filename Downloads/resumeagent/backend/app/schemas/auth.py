from pydantic import BaseModel, ConfigDict, EmailStr


class GitHubOAuthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    email: EmailStr
    github_token: str
