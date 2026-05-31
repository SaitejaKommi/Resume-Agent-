from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


REPO_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(REPO_ROOT / ".env", BACKEND_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "ResumeAgent"
    backend_url: AnyHttpUrl = "http://localhost:8000"
    frontend_url: AnyHttpUrl = "http://localhost:3000"
    database_url: str = Field(default="postgresql+asyncpg://resumeagent:resumeagent@localhost:5432/resumeagent")
    github_client_id: str = Field(default="")
    github_client_secret: str = Field(default="")
    github_redirect_uri: AnyHttpUrl = "http://localhost:8000/auth/github/callback"
    github_api_base_url: str = "https://api.github.com"
    groq_api_key: str = Field(default="")
    jwt_secret_key: str = Field(default="change_me")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    max_upload_size_mb: int = 5
    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
