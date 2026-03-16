"""empty message

Revision ID: 3c758a86a5fa
Revises: 7b4190e57466
Create Date: 2026-03-16 20:11:21.975286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c758a86a5fa'
down_revision: Union[str, Sequence[str], None] = '7b4190e57466'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
