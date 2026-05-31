"""phase1: add master_profiles, resume_versions, kanban_status

Revision ID: 0001_phase1
Revises: 
Create Date: 2026-05-31
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_phase1'
down_revision = '0000_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create master_profiles table
    op.create_table(
        'master_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('headline', sa.String(length=255), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('education_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('experience_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('skills_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('certifications_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('achievements_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('projects_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('github_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('portfolio_links_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column('profile_completeness', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('source_resume_id', sa.Integer(), sa.ForeignKey('resumes.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Create resume_versions table
    op.create_table(
        'resume_versions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('master_profile_id', sa.Integer(), sa.ForeignKey('master_profiles.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('application_id', sa.Integer(), sa.ForeignKey('applications.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('parent_version_id', sa.Integer(), sa.ForeignKey('resume_versions.id', ondelete='SET NULL'), nullable=True, index=True),
        sa.Column('version_name', sa.String(length=255), nullable=False),
        sa.Column('target_role', sa.String(length=255), nullable=True),
        sa.Column('resume_text', sa.Text(), nullable=False),
        sa.Column('resume_content_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('ats_score', sa.Float(), nullable=False, server_default='0'),
        sa.Column('ats_report_json', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    # Add kanban_status column to applications (nullable, default 'backlog')
    op.add_column('applications', sa.Column('kanban_status', sa.String(length=50), nullable=True))


def downgrade() -> None:
    # Drop kanban_status
    op.drop_column('applications', 'kanban_status')

    # Drop resume_versions and master_profiles
    op.drop_table('resume_versions')
    op.drop_table('master_profiles')
