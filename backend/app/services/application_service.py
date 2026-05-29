from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.application import Application
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User
from app.services.pipeline import run_mock_resume_job_pipeline


async def create_application(
    session: AsyncSession,
    user_id: int,
    resume_id: int,
    job_id: int,
    github_repos: list[str],
    pdf_path: str | None = None,
) -> Application:
    user_result = await session.execute(select(User.id).where(User.id == user_id))
    if user_result.scalar_one_or_none() is None:
        raise ValueError("User not found")

    resume_result = await session.execute(select(Resume).where(Resume.user_id == user_id, Resume.id == resume_id))
    resume = resume_result.scalar_one_or_none()
    job_result = await session.execute(select(Job).where(Job.user_id == user_id, Job.id == job_id))
    job = job_result.scalar_one_or_none()
    if resume is None or job is None:
        raise ValueError("Resume or job not found")

    pipeline_result = run_mock_resume_job_pipeline(resume.raw_text, job.jd_text, github_repos)
    application = Application(
        user_id=user_id,
        resume_id=resume_id,
        job_id=job_id,
        github_repos=github_repos,
        ats_score=pipeline_result["ats_score"],
        pdf_path=pdf_path,
        pipeline_result=pipeline_result,
    )
    session.add(application)
    await session.commit()
    await session.refresh(application)
    return application


async def list_user_applications(session: AsyncSession, user_id: int) -> list[Application]:
    result = await session.execute(select(Application).where(Application.user_id == user_id).order_by(Application.created_at.desc()))
    return list(result.scalars().all())


async def get_user_application(session: AsyncSession, user_id: int, application_id: int) -> Application | None:
    result = await session.execute(select(Application).where(Application.user_id == user_id, Application.id == application_id))
    return result.scalar_one_or_none()
