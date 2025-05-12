"""Clean up student table to retain required fields only

Revision ID: 8fc21ebfcb10
Revises: 32c4ee6e578b
Create Date: 2025-05-12 17:46:26.348996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fc21ebfcb10'
down_revision: Union[str, None] = '32c4ee6e578b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("students") as batch_op:
        batch_op.drop_column("maths")
        batch_op.drop_column("physics")
        batch_op.drop_column("chemistry")
        batch_op.drop_column("nata")
        batch_op.drop_column("studybreak")
        batch_op.drop_column("msc_cutoff")
        batch_op.drop_column("barch_cutoff")
        batch_op.drop_column("bdes_cutoff")
        batch_op.drop_column("applicationstatus")

def downgrade():
    with op.batch_alter_table("students") as batch_op:
        batch_op.add_column(sa.Column("maths", sa.Float))
        batch_op.add_column(sa.Column("physics", sa.Float))
        batch_op.add_column(sa.Column("chemistry", sa.Float))
        batch_op.add_column(sa.Column("nata", sa.Float))
        batch_op.add_column(sa.Column("studybreak", sa.Integer))
        batch_op.add_column(sa.Column("msc_cutoff", sa.Float))
        batch_op.add_column(sa.Column("barch_cutoff", sa.Float))
        batch_op.add_column(sa.Column("bdes_cutoff", sa.Float))
        batch_op.add_column(sa.Column("applicationstatus", sa.String))