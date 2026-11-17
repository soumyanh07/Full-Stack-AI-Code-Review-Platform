"""Create transactional indexing outbox.

Revision ID: 0002_indexing_outbox
Revises: 0001_repository_ownership
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_indexing_outbox"
down_revision = "0001_repository_ownership"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "outbox_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "repository_id",
            sa.Integer(),
            sa.ForeignKey("repositories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "event_type",
            sa.String(100),
            nullable=False,
            server_default="repository.index",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_error", sa.String(2000), nullable=True),
    )
    op.create_index(
        "ix_outbox_events_pending",
        "outbox_events",
        ["dispatched_at", "created_at"],
    )


def downgrade():
    op.drop_index("ix_outbox_events_pending", table_name="outbox_events")
    op.drop_table("outbox_events")
