"""Add degree column to students

Revision ID: abf1d84d8bce
Revises: c31b2e86fcc9
Create Date: 2025-05-12 17:37:06.984741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abf1d84d8bce'
down_revision: Union[str, None] = 'c31b2e86fcc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
