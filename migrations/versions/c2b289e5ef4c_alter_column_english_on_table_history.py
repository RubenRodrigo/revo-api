"""alter column english on table history

Revision ID: c2b289e5ef4c
Revises: e3f51ae5423f
Create Date: 2024-11-30 04:17:22.797302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2b289e5ef4c'
down_revision = 'e3f51ae5423f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('histories', schema=None) as batch_op:
        batch_op.alter_column(column_name='english_level', new_column_name='english')


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('histories', schema=None) as batch_op:
        batch_op.alter_column(column_name='english', new_column_name='english_level')

    # ### end Alembic commands ###
