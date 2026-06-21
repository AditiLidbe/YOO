"""Member Seeding

Revision ID: 1915022cbbf9
Revises: 0c070e1cccbf
Create Date: 2026-06-18 12:28:05.457628

"""
from typing import Sequence, Union
from app.utils.hashing import hash
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1915022cbbf9'
down_revision: Union[str, Sequence[str], None] = '0c070e1cccbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
   
    op.execute(f"""
        INSERT INTO members
(
    first_name,
    last_name,
    email,
    status,
    password,
    company_id
)
VALUES
(
    'ADITI',
    'LIDBE',
    'aditilidbe16@gmail.com',
    'ACTIVE',
    f"{hash('super123')}",
    '14'
)
        """)
    


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM members 
        WHERE email = 'aditilidbe16@gmail.com'
    """)

