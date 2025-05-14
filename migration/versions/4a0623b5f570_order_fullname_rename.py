"""Order fullname rename

Revision ID: 4a0623b5f570
Revises: d96db0eb36dd
Create Date: 2025-05-08 14:06:47.814123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a0623b5f570'
down_revision: Union[str, None] = 'd96db0eb36dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
