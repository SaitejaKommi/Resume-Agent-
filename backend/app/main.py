from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.models import Application, Job, MasterProfile, Resume, ResumeVersion, User
from app.routes import health
from app.routes import application, auth, download, job, profile, resume, resume_versions
from app.routes import version_ops, kanban_applications, profile_management

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins) + [str(settings.frontend_url)],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(job.router)
app.include_router(application.router)
app.include_router(profile.router)
app.include_router(resume_versions.router)
app.include_router(download.router)
app.include_router(version_ops.router)
app.include_router(kanban_applications.router)
app.include_router(profile_management.router)
