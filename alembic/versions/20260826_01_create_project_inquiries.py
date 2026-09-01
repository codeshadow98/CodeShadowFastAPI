"""create project inquiries

Revision ID: 20260826_01
Revises:
Create Date: 2026-08-26
"""
from alembic import op
import sqlalchemy as sa

revision = "20260826_01"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "project_inquiries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=False),
        sa.Column("company", sa.String(length=120), nullable=True),
        sa.Column("project_type", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("budget", sa.String(length=80), nullable=True),
        sa.Column("timeline", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_project_inquiries_email", "project_inquiries", ["email"])
    op.create_index("ix_project_inquiries_project_type", "project_inquiries", ["project_type"])

def downgrade() -> None:
    op.drop_index("ix_project_inquiries_project_type", table_name="project_inquiries")
    op.drop_index("ix_project_inquiries_email", table_name="project_inquiries")
    op.drop_table("project_inquiries")
