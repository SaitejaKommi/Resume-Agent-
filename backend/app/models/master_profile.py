from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MasterProfile(Base):
    __tablename__ = "master_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    headline: Mapped[str | None] = mapped_column(String(255), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    education_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    experience_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    skills_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    certifications_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    achievements_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    projects_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    github_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    portfolio_links_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    profile_completeness: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    source_resume_id: Mapped[int | None] = mapped_column(ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="master_profile")
    source_resume = relationship("Resume")
