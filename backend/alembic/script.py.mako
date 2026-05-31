"""
Revision ID: ${rev}
Revises: ${down_revision if down_revision else ""}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa

${upgrades if upgrades else "pass"}

${downgrades if downgrades else "pass"}
