from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    master_profile_id: Mapped[int] = mapped_column(ForeignKey("master_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    application_id: Mapped[int | None] = mapped_column(ForeignKey("applications.id", ondelete="SET NULL"), nullable=True, index=True)
    parent_version_id: Mapped[int | None] = mapped_column(ForeignKey("resume_versions.id", ondelete="SET NULL"), nullable=True, index=True)
    version_name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    resume_content_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    ats_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    ats_report_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User")
    master_profile = relationship("MasterProfile")
    application = relationship("Application", back_populates="resume_version", foreign_keys=[application_id])
    parent_version = relationship("ResumeVersion", remote_side=[id])
