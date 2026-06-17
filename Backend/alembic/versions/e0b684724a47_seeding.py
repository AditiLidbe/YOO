"""seed roles and super admin

Revision ID: e0b684724a47
Revises: e51aff7cc0b0
Create Date: 2026-06-10 12:38:04.825270

"""
import os
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0b684724a47'
down_revision: Union[str, Sequence[str], None] = 'e51aff7cc0b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()

    op.create_table(
        "member_role_mapping",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("member_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"]),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    role_names = [
        "SUPER_ADMIN",
        "ADMIN",
        "OWNER",
        "DEVELOPER",
        "COLLABORATOR",
    ]

    for role_name in role_names:
        existing_role = connection.execute(
            sa.text("select id from roles where name = :name"),
            {"name": role_name},
        ).first()

        if existing_role is None:
            connection.execute(
                sa.text("insert into roles (name) values (:name)"),
                {"name": role_name},
            )

    company_name = "Platform"
    existing_company = connection.execute(
        sa.text("select id from companys where name = :name"),
        {"name": company_name},
    ).first()

    if existing_company is None:
        connection.execute(
            sa.text(
                """
                insert into companys (name, logo, subcription)
                values (:name, :logo, :subcription)
                """
            ),
            {
                "name": company_name,
                "logo": "",
                "subcription": "ALL_FEATURE",
            },
        )

    company_id = connection.execute(
        sa.text("select id from companys where name = :name"),
        {"name": company_name},
    ).scalar_one()

    super_admin_email = os.getenv("SUPER_ADMIN_EMAIL", "admin@platform.com")
    existing_member = connection.execute(
        sa.text("select id from members where email = :email"),
        {"email": super_admin_email},
    ).first()

    if existing_member is None:
        connection.execute(
            sa.text(
                """
                insert into members
                (first_name, last_name, email, status, password, company_id)
                values
                (:first_name, :last_name, :email, :status, :password, :company_id)
                """
            ),
            {
                "first_name": "Super",
                "last_name": "Admin",
                "email": super_admin_email,
                "status": "ACTIVE",
                "password": None,
                "company_id": company_id,
            },
        )

    member_id = connection.execute(
        sa.text("select id from members where email = :email"),
        {"email": super_admin_email},
    ).scalar_one()

    role_id = connection.execute(
        sa.text("select id from roles where name = :name"),
        {"name": "SUPER_ADMIN"},
    ).scalar_one()

    existing_mapping = connection.execute(
        sa.text(
            """
            select id from member_role_mapping
            where member_id = :member_id and role_id = :role_id
            """
        ),
        {"member_id": member_id, "role_id": role_id},
    ).first()

    if existing_mapping is None:
        connection.execute(
            sa.text(
                """
                insert into member_role_mapping (member_id, role_id)
                values (:member_id, :role_id)
                """
            ),
            {"member_id": member_id, "role_id": role_id},
        )


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()
    super_admin_email = os.getenv("SUPER_ADMIN_EMAIL", "admin@platform.com")

    member_id = connection.execute(
        sa.text("select id from members where email = :email"),
        {"email": super_admin_email},
    ).scalar_one_or_none()

    if member_id is not None:
        connection.execute(
            sa.text("delete from member_role_mapping where member_id = :member_id"),
            {"member_id": member_id},
        )
        connection.execute(
            sa.text("delete from members where id = :member_id"),
            {"member_id": member_id},
        )

    connection.execute(
        sa.text(
            """
            delete from roles
            where name in (
                'SUPER_ADMIN',
                'ADMIN',
                'OWNER',
                'DEVELOPER',
                'COLLABORATOR'
            )
            """
        )
    )

    connection.execute(
        sa.text("delete from companys where name = :name"),
        {"name": "Platform"},
    )

    op.drop_table("member_role_mapping")
