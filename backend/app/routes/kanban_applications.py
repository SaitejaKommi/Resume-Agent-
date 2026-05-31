from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.application import Application
from app.services.application_service import list_user_applications, get_user_application

router = APIRouter(prefix="/kanban", tags=["kanban"])


@router.get("/list")
async def list_by_kanban(session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = await list_user_applications(session, current_user.id)
    columns: dict = {}
    for app in items:
        key = getattr(app, "kanban_status", None) or "backlog"
        columns.setdefault(key, []).append(app)
    return {"columns": columns}


@router.patch("/application/{id}/move")
async def move_application(id: int, kanban_status: str, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    app_obj = await get_user_application(session, current_user.id, id)
    if app_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    app_obj.kanban_status = kanban_status
    session.add(app_obj)
    await session.commit()
    await session.refresh(app_obj)
    return app_obj
