"""merge heads

Revision ID: 6154fcc58022
Revises: ad8f12b3456c, 6781e1659423
Create Date: 2026-03-22 11:11:50.909676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6154fcc58022'
down_revision: Union[str, None] = ('ad8f12b3456c', '6781e1659423')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
