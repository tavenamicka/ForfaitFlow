"""create clients table

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nom", sa.String(200), nullable=False),
        sa.Column("email", sa.String(255)),
        sa.Column("telephone", sa.String(30)),
        sa.Column("date_debut_contrat", sa.Date(), nullable=False),
        sa.Column("forfait_n1_h", sa.Integer(), server_default="4"),
        sa.Column("forfait_n2_h", sa.Integer(), server_default="3"),
        sa.Column("actif", sa.Boolean(), server_default=sa.true()),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("clients")
