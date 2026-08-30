"""Create sample_items table (disposable scaffold).

Revision ID: 0001
Revises:
Create Date: 2026-08-29
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = ("sample_module",)
depends_on: str | Sequence[str] | None = None

SEED_ID = "11111111-1111-1111-1111-111111111111"


def upgrade() -> None:
    op.create_table(
        "sample_items",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("message", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(
        sa.text(
            f"INSERT INTO sample_items (id, message) VALUES ('{SEED_ID}', 'Hello from Postgres')"
        )
    )


def downgrade() -> None:
    op.drop_table("sample_items")
