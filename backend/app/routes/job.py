from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user, get_current_user_optional
from app.db.session import get_db
from app.models.user import User
from app.schemas.job import JobCreate, JobListResponse, JobRead, JobUploadResponse
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
    current_user: User | None = Depends(get_current_user_optional),
) -> JobUploadResponse:
    if file.content_type not in {"text/plain", "application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only plain text or PDF job descriptions are supported")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File exceeds 5MB limit")

    jd_text = _extract_job_text(file, file_bytes)
    
    if current_user:
        job = await create_job(session, current_user.id, file.filename or "job-description", jd_text, extract_skills(jd_text))
        return JobUploadResponse(job_id=job.id)
    
    # For guest users, return temporary ID
    import hashlib
    temp_id = int(hashlib.md5(file_bytes[:100]).hexdigest(), 16) % 100000000
    return JobUploadResponse(job_id=temp_id)


@router.post("/upload/text", response_model=JobUploadResponse)
async def upload_job_text(
    payload: JobCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> JobUploadResponse:
    """Upload job description as plain text"""
    jd_text = payload.jd_text
    
    if current_user:
        job = await create_job(session, current_user.id, "job-description", jd_text, extract_skills(jd_text))
        return JobUploadResponse(job_id=job.id)
    
    # For guest users, return temporary ID
    import hashlib
    temp_id = int(hashlib.md5(jd_text.encode()).hexdigest(), 16) % 100000000
    return JobUploadResponse(job_id=temp_id)


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
