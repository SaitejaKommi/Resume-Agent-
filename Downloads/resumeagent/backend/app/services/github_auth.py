from urllib.parse import urlencode

import httpx
from github import Github
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.user import User


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


async def fetch_github_email(access_token: str, fallback_login: str) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            "https://api.github.com/user/emails",
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


async def upsert_github_user(session: Session, access_token: str) -> User:
    github = Github(access_token)
    profile = github.get_user()

    email = await fetch_github_email(access_token, profile.login)
    user = session.query(User).filter(User.email == email).one_or_none()
    if user is None:
        user = User(email=email, github_token=access_token)
        session.add(user)
    else:
        user.github_token = access_token

    session.commit()
    session.refresh(user)
    return user
