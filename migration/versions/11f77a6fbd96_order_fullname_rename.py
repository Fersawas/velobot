"""Order fullname rename

Revision ID: 11f77a6fbd96
Revises: 4a0623b5f570
Create Date: 2025-05-08 14:38:44.239286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11f77a6fbd96'
down_revision: Union[str, None] = '4a0623b5f570'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
