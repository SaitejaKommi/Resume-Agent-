import secrets

from fastapi import APIRouter, Cookie, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import GitHubOAuthResponse
from app.services.github_auth import build_github_authorization_url, exchange_code_for_token, upsert_github_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/github/login")
def github_login() -> RedirectResponse:
    state = secrets.token_urlsafe(32)
    response = RedirectResponse(url=build_github_authorization_url(state), status_code=307)
    response.set_cookie("github_oauth_state", state, httponly=True, samesite="lax", secure=False, max_age=600)
    return response


@router.get("/github/callback", response_model=GitHubOAuthResponse)
async def github_callback(
    code: str = Query(...),
    state: str = Query(...),
    stored_state: str | None = Cookie(default=None, alias="github_oauth_state"),
    db: Session = Depends(get_db),
) -> GitHubOAuthResponse:
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    access_token = await exchange_code_for_token(code)
    user = await upsert_github_user(db, access_token)
    return GitHubOAuthResponse(user_id=user.id, email=user.email, github_token=access_token)
