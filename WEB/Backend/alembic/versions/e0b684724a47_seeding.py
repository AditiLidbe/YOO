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
    pass

def downgrade() -> None:
    """Downgrade schema."""

    pass