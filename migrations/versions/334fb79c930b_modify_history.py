"""modify_history

Revision ID: 334fb79c930b
Revises: d4e662a9926e
Create Date: 2024-11-30 08:13:07.895850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '334fb79c930b'
down_revision = 'd4e662a9926e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('histories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('days', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('histories', schema=None) as batch_op:
        batch_op.drop_column('days')

    # ### end Alembic commands ###
