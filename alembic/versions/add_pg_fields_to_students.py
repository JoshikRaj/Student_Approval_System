"""Add PG fields for Student model

Revision ID: ad8f12b3456c
Revises: 147cfabc7964
Create Date: 2026-03-21 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ad8f12b3456c'
down_revision = '147cfabc7964'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('students') as batch_op:
        batch_op.add_column(sa.Column('program_type', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('ug_consolidated_mark', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('ug_course_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('ug_institution', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('tancet_gate_score', sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table('students') as batch_op:
        batch_op.drop_column('tancet_gate_score')
        batch_op.drop_column('ug_institution')
        batch_op.drop_column('ug_course_name')
        batch_op.drop_column('ug_consolidated_mark')
        batch_op.drop_column('program_type')
