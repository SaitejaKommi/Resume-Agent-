from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user, get_current_user_optional
from app.db.session import get_db
from app.models.user import User
from app.schemas.application import ApplicationCreate, ApplicationListResponse, ApplicationRead
from app.services.application_service import create_application, get_user_application, list_user_applications

router = APIRouter(prefix="/application", tags=["application"])


@router.post("/create", response_model=ApplicationRead)
async def create_user_application(
    payload: ApplicationCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> ApplicationRead:
    if current_user:
        try:
            return await create_application(
                session=session,
                user_id=current_user.id,
                resume_id=payload.resume_id,
                job_id=payload.job_id,
                github_repos=payload.github_repos,
                github_token=current_user.github_token or "",
                pdf_path=payload.pdf_path,
                company=payload.company,
                role_title=payload.role_title,
                status=payload.status,
                date_applied=payload.date_applied,
            )
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    else:
        # For guest users, return a mock response
        import hashlib
        from datetime import datetime
        
        mock_id = int(hashlib.md5(f"{payload.resume_id}{payload.job_id}".encode()).hexdigest(), 16) % 100000000
        return ApplicationRead(
            id=mock_id,
            user_id=0,
            resume_id=payload.resume_id,
            job_id=payload.job_id,
            company=payload.company or "Guest Company",
            role_title=payload.role_title or "Guest Role",
            status=payload.status or "saved",
            date_applied=payload.date_applied or datetime.now(),
            resume_version_id=None,
            github_repos=payload.github_repos,
            ats_score=0.0,
            pdf_path=payload.pdf_path,
            pipeline_result={},
            created_at=datetime.now(),
        )


@router.get("/{id}", response_model=ApplicationRead)
async def read_application(
    id: int,
    session: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> ApplicationRead:
    if current_user:
        application = await get_user_application(session, current_user.id, id)
        if application is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
        return application
    else:
        # For guest users, return mock application data
        # In a real app, this would need to be stored somewhere (cache, session, etc.)
        # For now, return a mock with processing status
        import hashlib
        from datetime import datetime
        
        return ApplicationRead(
            id=id,
            user_id=0,
            resume_id=1,
            job_id=1,
            company="Guest Company",
            role_title="Guest Role",
            status="saved",
            date_applied=datetime.now(),
            resume_version_id=None,
            github_repos=[],
            ats_score=78.5,  # Mock ATS score
            pdf_path=None,
            pipeline_result={"status": "completed"},
            created_at=datetime.now(),
        )


@router.get("/list", response_model=ApplicationListResponse)
async def list_applications(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ApplicationListResponse:
    items = await list_user_applications(session, current_user.id)
    return ApplicationListResponse(items=items)
