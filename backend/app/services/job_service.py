from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.user import User
from app.services.file_extractors import extract_pdf_text, extract_plain_text


async def create_job(session: AsyncSession, user_id: int, filename: str, jd_text: str, extracted_skills: list[str] | None = None) -> Job:
    result = await session.execute(select(User.id).where(User.id == user_id))
    if result.scalar_one_or_none() is None:
        raise ValueError("User not found")

    job = Job(user_id=user_id, filename=filename, jd_text=jd_text, extracted_skills=extracted_skills or [])
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job


async def list_user_jobs(session: AsyncSession, user_id: int) -> list[Job]:
    result = await session.execute(select(Job).where(Job.user_id == user_id).order_by(Job.created_at.desc()))
    return list(result.scalars().all())


async def get_user_job(session: AsyncSession, user_id: int, job_id: int) -> Job | None:
    result = await session.execute(select(Job).where(Job.user_id == user_id, Job.id == job_id))
    return result.scalar_one_or_none()


def normalize_job_text(file_bytes: bytes, content_type: str | None) -> str:
    if content_type == "application/pdf":
        return extract_pdf_text(file_bytes)
    return extract_plain_text(file_bytes)
