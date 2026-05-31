from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.resume_version_service import (
    get_user_resume_version,
    create_resume_version,
    list_user_resume_versions,
)

router = APIRouter(prefix="/versions", tags=["versions"])


@router.post("/{id}/clone")
async def clone_version(id: int, new_name: str, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    src = await get_user_resume_version(session, current_user.id, id)
    if src is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found")

    clone = await create_resume_version(
        session,
        user_id=current_user.id,
        master_profile_id=src.master_profile_id,
        application_id=None,
        version_name=new_name or f"{src.version_name} (copy)",
        target_role=src.target_role,
        resume_text=src.resume_text,
        resume_content_json=src.resume_content_json,
        ats_score=src.ats_score or 0.0,
        ats_report_json=src.ats_report_json or {},
        parent_version_id=src.id,
    )
    return clone


@router.get("/{id}/diff/{other_id}")
async def diff_versions(id: int, other_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    v1 = await get_user_resume_version(session, current_user.id, id)
    v2 = await get_user_resume_version(session, current_user.id, other_id)
    if v1 is None or v2 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found")

    # Simple diff: report keys that differ in resume_content_json
    a = v1.resume_content_json or {}
    b = v2.resume_content_json or {}
    diffs = {}
    keys = set(a.keys()) | set(b.keys())
    for k in keys:
        if a.get(k) != b.get(k):
            diffs[k] = {"from": a.get(k), "to": b.get(k)}
    return {"diff": diffs}


@router.patch("/{id}/rename")
async def rename_version(id: int, new_name: str, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    v = await get_user_resume_version(session, current_user.id, id)
    if v is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found")
    v.version_name = new_name
    session.add(v)
    await session.commit()
    await session.refresh(v)
    return v
