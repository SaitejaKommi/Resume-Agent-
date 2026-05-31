from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
from github import Github
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.user import User
from app.services.profile_service import upsert_github_metadata


settings = get_settings()


def build_github_authorization_url(state: str) -> str:
    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": str(settings.github_redirect_uri),
        "scope": "read:user user:email",
        "state": state,
        "allow_signup": "true",
    }
    return f"https://github.com/login/oauth/authorize?{urlencode(params)}"


async def exchange_code_for_token(code: str) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_uri": str(settings.github_redirect_uri),
            },
        )
        response.raise_for_status()
        payload = response.json()
        access_token = payload.get("access_token")
        if not access_token:
            raise ValueError("GitHub did not return an access token")
        return access_token


def create_access_token(user_id: int, email: str) -> tuple[str, int]:
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire_at = datetime.now(timezone.utc) + expires_delta
    token = jwt.encode(
        {"sub": str(user_id), "email": email, "exp": expire_at},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return token, int(expires_delta.total_seconds())


async def fetch_github_email(access_token: str, fallback_login: str) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{settings.github_api_base_url}/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        if response.status_code == 200:
            for email_record in response.json():
                if email_record.get("primary"):
                    email_value = email_record.get("email")
                    if email_value:
                        return email_value
        return f"{fallback_login}@users.noreply.github.com"


async def upsert_github_user(session: AsyncSession, access_token: str) -> User:
    github = Github(access_token)
    profile = github.get_user()
    email = await fetch_github_email(access_token, profile.login)

    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(email=email, github_token=access_token)
        session.add(user)
    else:
        user.github_token = access_token

    await session.commit()
    await session.refresh(user)

    github_json = {
        "login": profile.login,
        "name": profile.name,
        "bio": profile.bio,
        "company": profile.company,
        "location": profile.location,
        "blog": profile.blog,
        "html_url": profile.html_url,
        "public_repos": profile.public_repos,
        "followers": profile.followers,
        "following": profile.following,
    }
    await upsert_github_metadata(session, user.id, github_json)
    return user
