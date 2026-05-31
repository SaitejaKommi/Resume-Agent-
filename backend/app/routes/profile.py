from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.profile import MasterProfileRead, MasterProfileUpdate
from app.services.profile_service import get_user_master_profile, update_master_profile

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/me", response_model=MasterProfileRead | None)
async def read_profile(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MasterProfileRead | None:
    return await get_user_master_profile(session, current_user.id)


@router.patch("/me", response_model=MasterProfileRead)
async def patch_profile(
    payload: MasterProfileUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MasterProfileRead:
    return await update_master_profile(session, current_user.id, payload.model_dump(exclude_unset=True))
