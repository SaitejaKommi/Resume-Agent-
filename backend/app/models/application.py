from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="saved", nullable=False)
    date_applied: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resume_version_id: Mapped[int | None] = mapped_column(ForeignKey("resume_versions.id", ondelete="SET NULL"), nullable=True, index=True)
    github_repos: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    ats_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    pdf_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    pipeline_result: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    resume_version = relationship("ResumeVersion", back_populates="application", foreign_keys=[resume_version_id], uselist=False)
