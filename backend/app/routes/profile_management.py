from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.master_profile import MasterProfile
from app.services.profile_service import (
    get_user_master_profile,
    upsert_master_profile_from_resume,
    upsert_github_metadata,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/me", response_model=object)
async def get_my_profile(session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    p = await get_user_master_profile(session, current_user.id)
    return p


@router.post("/me/from_resume")
async def create_profile_from_resume(resume_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    # fetch resume and upsert profile
    from app.models.resume import Resume

    result = await session.execute(select(Resume).where(Resume.user_id == current_user.id, Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    profile = await upsert_master_profile_from_resume(session, current_user.id, resume)
    return profile


@router.post("/me/cache_github")
async def cache_github(metadata: dict, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = await upsert_github_metadata(session, current_user.id, metadata)
    return profile


@router.get("/list")
async def list_profiles(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(MasterProfile))
    return list(result.scalars().all())
