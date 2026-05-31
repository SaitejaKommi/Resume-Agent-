from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.master_profile import MasterProfile
from app.models.resume import Resume
from app.models.user import User


def _profile_completeness(profile: MasterProfile) -> int:
    checks = [
        bool(profile.summary),
        bool(profile.education_json),
        bool(profile.experience_json),
        bool(profile.skills_json),
        bool(profile.projects_json),
        bool(profile.portfolio_links_json),
        bool(profile.github_json),
    ]
    return round((sum(checks) / len(checks)) * 100)


def _resume_profile_sections(resume: Resume) -> dict:
    data = resume.json_data or {}
    return {
        "summary": data.get("summary"),
        "education_json": data.get("education") or data.get("raw_education") or [],
        "experience_json": data.get("experience") or data.get("raw_experience") or [],
        "skills_json": data.get("skills") or [],
        "certifications_json": data.get("certifications") or [],
        "achievements_json": data.get("achievements") or [],
        "projects_json": data.get("projects") or [],
        "portfolio_links_json": data.get("portfolio_links") or [],
    }


async def ensure_master_profile(session: AsyncSession, user_id: int) -> MasterProfile:
    result = await session.execute(select(MasterProfile).where(MasterProfile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if profile is not None:
        return profile

    user_result = await session.execute(select(User.id).where(User.id == user_id))
    if user_result.scalar_one_or_none() is None:
        raise ValueError("User not found")

    profile = MasterProfile(user_id=user_id)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def upsert_master_profile_from_resume(session: AsyncSession, user_id: int, resume: Resume) -> MasterProfile:
    profile = await ensure_master_profile(session, user_id)
    sections = _resume_profile_sections(resume)

    profile.summary = sections["summary"] or profile.summary
    profile.education_json = sections["education_json"] or profile.education_json
    profile.experience_json = sections["experience_json"] or profile.experience_json
    profile.skills_json = sections["skills_json"] or profile.skills_json
    profile.certifications_json = sections["certifications_json"] or profile.certifications_json
    profile.achievements_json = sections["achievements_json"] or profile.achievements_json
    profile.projects_json = sections["projects_json"] or profile.projects_json
    profile.portfolio_links_json = sections["portfolio_links_json"] or profile.portfolio_links_json
    profile.source_resume_id = resume.id
    profile.profile_completeness = _profile_completeness(profile)

    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def upsert_github_metadata(session: AsyncSession, user_id: int, github_json: dict) -> MasterProfile:
    profile = await ensure_master_profile(session, user_id)
    profile.github_json = github_json
    profile.profile_completeness = _profile_completeness(profile)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def update_master_profile(session: AsyncSession, user_id: int, updates: dict) -> MasterProfile:
    profile = await ensure_master_profile(session, user_id)
    for field_name, value in updates.items():
        if value is not None and hasattr(profile, field_name):
            setattr(profile, field_name, value)
    profile.profile_completeness = _profile_completeness(profile)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def get_user_master_profile(session: AsyncSession, user_id: int) -> MasterProfile | None:
    result = await session.execute(
        select(MasterProfile)
        .options(selectinload(MasterProfile.source_resume))
        .where(MasterProfile.user_id == user_id)
    )
    return result.scalar_one_or_none()
