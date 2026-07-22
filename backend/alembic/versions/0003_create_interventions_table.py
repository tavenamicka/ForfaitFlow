"""create interventions table

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "interventions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("client_id", sa.Integer(), sa.ForeignKey("clients.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("date_intervention", sa.Date(), nullable=False),
        sa.Column("niveau", sa.String(2), nullable=False),
        sa.Column("duree_minutes", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("groupe_id", postgresql.UUID(as_uuid=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("niveau IN ('N1', 'N2', 'N3')", name="ck_interventions_niveau"),
        sa.CheckConstraint("duree_minutes > 0", name="ck_interventions_duree_positive"),
    )
    op.create_index("idx_interventions_client_date", "interventions", ["client_id", "date_intervention"])
    op.create_index(
        "idx_interventions_groupe",
        "interventions",
        ["groupe_id"],
        postgresql_where=sa.text("groupe_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("idx_interventions_groupe", table_name="interventions")
    op.drop_index("idx_interventions_client_date", table_name="interventions")
    op.drop_table("interventions")
