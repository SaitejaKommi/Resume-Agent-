from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume
from app.models.user import User
from app.services.profile_service import upsert_master_profile_from_resume


async def create_resume(session: AsyncSession, user_id: int, filename: str, raw_text: str, json_data: dict | None = None) -> Resume:
    result = await session.execute(select(User.id).where(User.id == user_id))
    if result.scalar_one_or_none() is None:
        raise ValueError("User not found")

    resume = Resume(user_id=user_id, filename=filename, raw_text=raw_text, json_data=json_data or {})
    session.add(resume)
    await session.commit()
    await session.refresh(resume)
    await upsert_master_profile_from_resume(session, user_id, resume)
    return resume


async def list_user_resumes(session: AsyncSession, user_id: int) -> list[Resume]:
    result = await session.execute(select(Resume).where(Resume.user_id == user_id).order_by(Resume.created_at.desc()))
    return list(result.scalars().all())


async def get_user_resume(session: AsyncSession, user_id: int, resume_id: int) -> Resume | None:
    result = await session.execute(select(Resume).where(Resume.user_id == user_id, Resume.id == resume_id))
    return result.scalar_one_or_none()
