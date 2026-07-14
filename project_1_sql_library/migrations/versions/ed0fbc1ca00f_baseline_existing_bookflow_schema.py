"""
baseline existing BookFlow schema
Revision ID: ed0fbc1ca00f
Create Date: 2026-07-11 19:54:30.566593
"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = 'ed0fbc1ca00f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
