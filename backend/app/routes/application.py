from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationListResponse, ApplicationRead
from app.services.application_service import create_application, get_user_application, list_user_applications

router = APIRouter(prefix="/application", tags=["application"])


@router.post("/create", response_model=ApplicationRead)
async def create_user_application(
    payload: ApplicationCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApplicationRead:
    try:
        return await create_application(
            session=session,
            user_id=current_user.id,
            resume_id=payload.resume_id,
            job_id=payload.job_id,
            github_repos=payload.github_repos,
            github_token=current_user.github_token or "",
            pdf_path=payload.pdf_path,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{id}", response_model=ApplicationRead)
async def read_application(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApplicationRead:
    application = await get_user_application(session, current_user.id, id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.get("/list", response_model=ApplicationListResponse)
async def list_applications(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApplicationListResponse:
    items = await list_user_applications(session, current_user.id)
    return ApplicationListResponse(items=items)
