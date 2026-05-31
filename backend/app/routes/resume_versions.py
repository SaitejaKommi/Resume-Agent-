from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.resume_version import ResumeVersionListResponse, ResumeVersionRead
from app.services.resume_version_service import get_user_resume_version, list_user_resume_versions

router = APIRouter(prefix="/resume-versions", tags=["resume-versions"])


@router.get("/list", response_model=ResumeVersionListResponse)
async def list_versions(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeVersionListResponse:
    items = await list_user_resume_versions(session, current_user.id)
    return ResumeVersionListResponse(items=items)


@router.get("/{version_id}", response_model=ResumeVersionRead)
async def read_version(
    version_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeVersionRead:
    version = await get_user_resume_version(session, current_user.id, version_id)
    if version is None:
        raise HTTPException(status_code=404, detail="Resume version not found")
    return version
