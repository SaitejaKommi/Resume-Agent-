from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ai.resume_generator import generate_pdf
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.application import Application
from app.models.user import User
from app.services.application_service import get_user_application

router = APIRouter(prefix="", tags=["download"])


def _pdf_storage_dir() -> Path:
    return Path(__file__).resolve().parents[3] / "generated_pdfs"


def _application_pdf_path(application_id: int) -> Path:
    return _pdf_storage_dir() / f"application_{application_id}.pdf"


def _build_resume_payload(application: Application) -> dict:
    resume_json = application.resume.json_data or {}
    personal = resume_json.get("personal") or resume_json.get("personal_info") or {}
    projects = resume_json.get("projects") or []
    experience = resume_json.get("experience") or []
    education = resume_json.get("education") or []
    skills = resume_json.get("skills") or {}

    if isinstance(skills, list):
        skills = {"Core": skills}

    if not personal:
        personal = {
            "name": resume_json.get("name") or "ResumeAgent User",
            "email": resume_json.get("email") or "",
            "phone": resume_json.get("phone") or "",
            "github": resume_json.get("github") or "",
            "linkedin": resume_json.get("linkedin") or "",
            "portfolio": resume_json.get("portfolio") or "",
        }

    if not projects and application.pipeline_result:
        pipeline_projects = application.pipeline_result.get("projects") or []
        projects = [
            {
                **project,
                "tech_tags": project.get("tech_tags") or project.get("tech_stack") or [],
            }
            for project in pipeline_projects
        ]

    if not experience and resume_json.get("raw_experience"):
        experience = resume_json["raw_experience"]

    if not education and resume_json.get("raw_education"):
        education = resume_json["raw_education"]

    return {
        "personal": personal,
        "skills": skills,
        "projects": projects,
        "experience": experience,
        "education": education,
        "summary": resume_json.get("summary") or application.pipeline_result.get("summary") or "",
    }


@router.get("/download/{application_id}")
async def download_application_pdf(
    application_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FileResponse:
    application = await get_user_application(session, current_user.id, application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    pdf_path = Path(application.pdf_path) if application.pdf_path else _application_pdf_path(application.id)
    if not pdf_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF not generated yet")

    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename=pdf_path.name,
    )


@router.post("/generate/{application_id}")
async def generate_application_pdf(
    application_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    application = await get_user_application(session, current_user.id, application_id)
    if application is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    pdf_path = Path(application.pdf_path) if application.pdf_path else _application_pdf_path(application.id)
    if pdf_path.exists():
        if application.pdf_path != str(pdf_path):
            application.pdf_path = str(pdf_path)
            session.add(application)
            await session.commit()
        return {"pdf_url": f"/download/{application.id}"}

    resume_payload = _build_resume_payload(application)
    generated_path = generate_pdf(resume_payload, str(pdf_path))
    application.pdf_path = generated_path
    session.add(application)
    await session.commit()

    return {"pdf_url": f"/download/{application.id}"}