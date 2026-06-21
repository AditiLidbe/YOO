"""Role Seeding

Revision ID: 1eae35f0a681
Revises: 1915022cbbf9
Create Date: 2026-06-18 12:31:51.134704

"""
from typing import Sequence, Union
from sqlalchemy.sql import table, column
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1eae35f0a681'
down_revision: Union[str, Sequence[str], None] = '1915022cbbf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None






def upgrade() -> None:
    
    roles_table = table(
        'roles',
        column('name', sa.String)
    )

    
    op.bulk_insert(
        roles_table,
        [
            {'name': 'SUPER_ADMIN'},
            {'name': 'ADMIN'},
            {'name': 'OWNER'},
            {'name': 'DEVELOPER'},
            {'name': 'COLLABORATOR'},

        ]
    )  


def downgrade() -> None:
    roles_table = table('roles', column('name', sa.String))
    op.execute(
        roles_table.delete().where(
            roles_table.c.name.in_([
                'SUPER_ADMIN', 'ADMIN', 'OWNER', 'DEVELOPER', 'COLLABORATOR'
            ])
        )
    )