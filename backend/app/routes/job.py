from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.job import JobListResponse, JobRead, JobUploadResponse
from app.services.file_extractors import extract_pdf_text, extract_plain_text
from app.services.job_service import create_job, get_user_job, list_user_jobs
from ai.skill_extractor import extract_skills

router = APIRouter(prefix="/job", tags=["job"])
MAX_BYTES = 5 * 1024 * 1024


def _extract_job_text(upload: UploadFile, file_bytes: bytes) -> str:
    if upload.content_type == "application/pdf" or (upload.filename or "").lower().endswith(".pdf"):
        return extract_pdf_text(file_bytes)
    return extract_plain_text(file_bytes)


@router.post("/upload", response_model=JobUploadResponse)
async def upload_job(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobUploadResponse:
    if file.content_type not in {"text/plain", "application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only plain text or PDF job descriptions are supported")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File exceeds 5MB limit")

    jd_text = _extract_job_text(file, file_bytes)
    job = await create_job(session, current_user.id, file.filename or "job-description", jd_text, extract_skills(jd_text))
    return JobUploadResponse(job_id=job.id)


@router.get("/{id}", response_model=JobRead)
async def read_job(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobRead:
    job = await get_user_job(session, current_user.id, id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job
