"""Initial schema revision

Revision ID: 001_initial
Revises:
Create Date: 2026-11-04 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from app.database.base import Base

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use metadata create_all for initial schema
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
