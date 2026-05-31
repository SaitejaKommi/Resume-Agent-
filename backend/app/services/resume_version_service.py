from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.resume_version import ResumeVersion
from app.models.user import User


async def create_resume_version(
    session: AsyncSession,
    *,
    user_id: int,
    master_profile_id: int,
    application_id: int | None,
    version_name: str,
    target_role: str | None,
    resume_text: str,
    resume_content_json: dict,
    ats_score: float,
    ats_report_json: dict,
    parent_version_id: int | None = None,
) -> ResumeVersion:
    user_result = await session.execute(select(User.id).where(User.id == user_id))
    if user_result.scalar_one_or_none() is None:
        raise ValueError("User not found")

    version = ResumeVersion(
        user_id=user_id,
        master_profile_id=master_profile_id,
        application_id=application_id,
        parent_version_id=parent_version_id,
        version_name=version_name,
        target_role=target_role,
        resume_text=resume_text,
        resume_content_json=resume_content_json,
        ats_score=ats_score,
        ats_report_json=ats_report_json,
    )
    session.add(version)
    await session.commit()
    await session.refresh(version)
    return version


async def list_user_resume_versions(session: AsyncSession, user_id: int) -> list[ResumeVersion]:
    result = await session.execute(
        select(ResumeVersion)
        .options(selectinload(ResumeVersion.application))
        .where(ResumeVersion.user_id == user_id)
        .order_by(ResumeVersion.created_at.desc())
    )
    return list(result.scalars().all())


async def get_user_resume_version(session: AsyncSession, user_id: int, version_id: int) -> ResumeVersion | None:
    result = await session.execute(
        select(ResumeVersion)
        .where(ResumeVersion.user_id == user_id, ResumeVersion.id == version_id)
    )
    return result.scalar_one_or_none()
