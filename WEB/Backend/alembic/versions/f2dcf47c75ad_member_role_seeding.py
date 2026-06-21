"""Member  Role Seeding

Revision ID: f2dcf47c75ad
Revises: 1eae35f0a681
Create Date: 2026-06-18 13:24:03.621696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2dcf47c75ad'
down_revision: Union[str, Sequence[str], None] = '1eae35f0a681'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(f"""
               INSERT INTO member_role_mapping
(
    member_id,
    role_id
)
VALUES
(
    
    1,
    1
)
        """)
    
def downgrade() -> None:
    
    op.execute("""
        DELETE FROM member_role_mapping 
        WHERE member_id = 1 AND role_id = 1
    """)
    
    


