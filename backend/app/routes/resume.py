from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import get_current_user, get_current_user_optional
from app.db.session import get_db
from app.models.user import User
from app.schemas.resume import ResumeListResponse, ResumeRead, ResumeUploadResponse
from app.services.file_extractors import extract_docx_text, extract_pdf_text, extract_plain_text
from app.services.resume_service import create_resume, get_user_resume, list_user_resumes

router = APIRouter(prefix="/resume", tags=["resume"])
settings = get_settings()
MAX_BYTES = settings.max_upload_size_mb * 1024 * 1024


def _extract_text(upload: UploadFile, file_bytes: bytes) -> str:
    suffix = Path(upload.filename or "").suffix.lower()
    content_type = upload.content_type or ""
    if content_type == "application/pdf" or suffix == ".pdf":
        return extract_pdf_text(file_bytes)
    if content_type in {"application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"} or suffix == ".docx":
        return extract_docx_text(file_bytes)
    return extract_plain_text(file_bytes)


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> ResumeUploadResponse:
    if file.content_type not in {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
        "text/plain",
        "application/octet-stream",
    }:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only PDF or DOCX files are supported")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File exceeds 5MB limit")

    raw_text = _extract_text(file, file_bytes)
    
    # If user is authenticated, store in database
    if current_user:
        resume = await create_resume(session, current_user.id, file.filename or "resume", raw_text)
        return ResumeUploadResponse(resume_id=resume.id)
    
    # For guest users, return a temporary ID based on hash
    # In production, consider using temporary storage or sessions
    import hashlib
    temp_id = int(hashlib.md5(file_bytes[:100]).hexdigest(), 16) % 100000000
    return ResumeUploadResponse(resume_id=temp_id)


@router.get("/{id}", response_model=ResumeRead)
async def read_resume(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeRead:
    resume = await get_user_resume(session, current_user.id, id)
    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return resume


@router.get("/list", response_model=list[ResumeRead])
async def list_resumes(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ResumeRead]:
    return await list_user_resumes(session, current_user.id)
