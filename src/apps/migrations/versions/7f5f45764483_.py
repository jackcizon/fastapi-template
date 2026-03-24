"""empty message

Revision ID: 7f5f45764483
Revises: 3c758a86a5fa
Create Date: 2026-03-16 22:01:05.371264

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7f5f45764483"
down_revision: Union[str, Sequence[str], None] = "3c758a86a5fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
