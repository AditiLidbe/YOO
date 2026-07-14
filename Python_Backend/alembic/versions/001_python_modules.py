"""Create Python module tables

Revision ID: 001_python_modules
Revises:
Create Date: 2026-07-15
"""

from alembic import op
import sqlalchemy as sa


revision = "001_python_modules"
down_revision = None
branch_labels = None
depends_on = None


job_status = sa.Enum("DRAFT", "OPEN", "CLOSED", name="jobstatus")
application_status = sa.Enum(
    "APPLIED",
    "UNDER_AI_REVIEW",
    "UNDER_RECRUITER_REVIEW",
    "INTERVIEW",
    "OFFER",
    "REJECTED",
    "HOLD",
    name="applicationstatus",
)
ai_status = sa.Enum("PENDING", "COMPLETED", "FAILED", name="aistatus")
ai_recommendation = sa.Enum(
    "STRONG_FIT",
    "POSSIBLE_FIT",
    "NOT_FIT",
    name="airecommendation",
)
ai_check_type = sa.Enum(
    "SKILL",
    "EXPERIENCE",
    "COVER_LETTER",
    "COMPLETENESS",
    name="aichecktype",
)


def upgrade():
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("requirements", sa.Text(), nullable=False),
        sa.Column("department", sa.String(length=150), nullable=False),
        sa.Column("experience_required", sa.Integer(), nullable=True),
        sa.Column("job_role", sa.String(length=150), nullable=True),
        sa.Column("status", job_status, nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("recruiters.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey("jobs.id"), nullable=False),
        sa.Column("resume", sa.String(length=500), nullable=True),
        sa.Column("cover_letter", sa.Text(), nullable=True),
        sa.Column("status", application_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ai",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id"), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("recommendation", ai_recommendation, nullable=True),
        sa.Column("status", ai_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "ai_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("ai_id", sa.Integer(), sa.ForeignKey("ai.id"), nullable=False),
        sa.Column("check_type", ai_check_type, nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("comments", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("ai_results")
    op.drop_table("ai")
    op.drop_table("applications")
    op.drop_table("jobs")
    ai_check_type.drop(op.get_bind(), checkfirst=True)
    ai_recommendation.drop(op.get_bind(), checkfirst=True)
    ai_status.drop(op.get_bind(), checkfirst=True)
    application_status.drop(op.get_bind(), checkfirst=True)
    job_status.drop(op.get_bind(), checkfirst=True)
