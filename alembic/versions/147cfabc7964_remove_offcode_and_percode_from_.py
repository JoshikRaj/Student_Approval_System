"""Remove offcode and percode from recommenders table

Revision ID: 147cfabc7964
Revises: 8fc21ebfcb10
Create Date: 2025-05-12 17:53:10.458335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '147cfabc7964'
down_revision: Union[str, None] = '8fc21ebfcb10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op

def upgrade():
    with op.batch_alter_table("recommenders") as batch_op:
        batch_op.drop_column("offcode")
        batch_op.drop_column("percode")

def downgrade():
    with op.batch_alter_table("recommenders") as batch_op:
        batch_op.add_column(sa.Column("offcode", sa.String))
        batch_op.add_column(sa.Column("percode", sa.String))
