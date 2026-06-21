"""Permission seeding and role seeding

Revision ID: 0c070e1cccbf
Revises: 70f305879d56
Create Date: 2026-06-18 11:25:38.181123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from  app.utils.config import setting

# revision identifiers, used by Alembic.
revision: str = '0c070e1cccbf'
down_revision: Union[str, Sequence[str], None] = '70f305879d56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(f"""
        INSERT INTO companys
(
    name,
    logo,
    subcription,
    domain
    
)
VALUES
(
    'ZOHO',
    'zoho.file',
    'ALL_FEATURE',
    'zoho.com'
    
)
        """)
    
    

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DELETE FROM members 
        WHERE name = 'ZOHO'
    """)