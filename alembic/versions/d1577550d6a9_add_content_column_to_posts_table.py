"""add content column to posts table

Revision ID: d1577550d6a9
Revises: bf5a50c25f35
Create Date: 2026-02-13 19:06:55.030270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1577550d6a9'
down_revision: Union[str, Sequence[str], None] = 'bf5a50c25f35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
