"""Add repository ownership.

Revision ID: 0001_repository_ownership
Revises:
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_repository_ownership"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()

    existing_count = bind.execute(
        sa.text("SELECT COUNT(*) FROM repositories")
    ).scalar_one()

    if existing_count:
        raise RuntimeError(
            "Ownership migration stopped: repositories already exist. "
            "Assign verified owners before migrating."
        )

    op.add_column(
        "repositories",
        sa.Column("owner_id", sa.Integer(), nullable=False),
    )

    op.create_foreign_key(
        "fk_repositories_owner_id_users",
        "repositories",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        "repositories_url_key",
        "repositories",
        type_="unique",
    )

    op.create_index(
        "ix_repositories_owner_id",
        "repositories",
        ["owner_id"],
    )

    op.create_unique_constraint(
        "uq_repositories_owner_url",
        "repositories",
        ["owner_id", "url"],
    )


def downgrade():
    op.drop_constraint(
        "uq_repositories_owner_url",
        "repositories",
        type_="unique",
    )

    op.drop_index(
        "ix_repositories_owner_id",
        table_name="repositories",
    )

    op.drop_constraint(
        "fk_repositories_owner_id_users",
        "repositories",
        type_="foreignkey",
    )

    op.drop_column(
        "repositories",
        "owner_id",
    )

    op.create_unique_constraint(
        "repositories_url_key",
        "repositories",
        ["url"],
    )
