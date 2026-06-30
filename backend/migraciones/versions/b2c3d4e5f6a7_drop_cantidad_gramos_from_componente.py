"""drop cantidad_gramos from componente (existencias ahora es en gramos)

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-06-29 00:00:01.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "b2c3d4e5f6a7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("componente", "cantidad_gramos")


def downgrade() -> None:
    op.add_column(
        "componente",
        sa.Column("cantidad_gramos", sa.Integer(), nullable=False, server_default="0"),
    )
