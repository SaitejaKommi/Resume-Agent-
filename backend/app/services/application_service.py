from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.application import Application
from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User
from app.services.profile_service import ensure_master_profile
from app.services.resume_version_service import create_resume_version
from app.services.pipeline import run_mock_resume_job_pipeline


async def create_application(
    session: AsyncSession,
    user_id: int,
    resume_id: int,
    job_id: int,
    github_repos: list[str],
    github_token: str,
    pdf_path: str | None = None,
    company: str | None = None,
    role_title: str | None = None,
    status: str = "saved",
    date_applied=None,
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

    profile = await ensure_master_profile(session, user_id)

    pipeline_result = run_mock_resume_job_pipeline(resume.raw_text, job.jd_text, github_repos, github_token)
    resume_version = await create_resume_version(
        session,
        user_id=user_id,
        master_profile_id=profile.id,
        application_id=None,
        version_name=f"{company or role_title or job.filename or 'Application'} v1",
        target_role=role_title or job.filename,
        resume_text=resume.raw_text,
        resume_content_json={
            "resume": resume.json_data,
            "pipeline_result": pipeline_result,
            "job": {
                "id": job.id,
                "filename": job.filename,
                "jd_text": job.jd_text,
            },
        },
        ats_score=pipeline_result["ats_score"],
        ats_report_json={
            "missing_keywords": pipeline_result.get("missing_keywords", []),
            "suggestions": pipeline_result.get("suggestions", []),
        },
    )
    application = Application(
        user_id=user_id,
        resume_id=resume_id,
        job_id=job_id,
        company=company,
        role_title=role_title or job.filename,
        status=status,
        date_applied=date_applied,
        resume_version_id=resume_version.id,
        github_repos=github_repos,
        ats_score=pipeline_result["ats_score"],
        pdf_path=pdf_path,
        pipeline_result=pipeline_result,
    )
    session.add(application)
    await session.commit()
    await session.refresh(application)
    resume_version.application_id = application.id
    session.add(resume_version)
    await session.commit()
    return application


async def list_user_applications(session: AsyncSession, user_id: int) -> list[Application]:
    result = await session.execute(
        select(Application)
        .options(selectinload(Application.resume), selectinload(Application.job), selectinload(Application.resume_version))
        .where(Application.user_id == user_id)
        .order_by(Application.created_at.desc())
    )
    return list(result.scalars().all())


async def get_user_application(session: AsyncSession, user_id: int, application_id: int) -> Application | None:
    result = await session.execute(
        select(Application)
        .options(selectinload(Application.resume), selectinload(Application.job), selectinload(Application.resume_version))
        .where(Application.user_id == user_id, Application.id == application_id)
    )
    return result.scalar_one_or_none()
