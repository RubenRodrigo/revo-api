"""add result column

Revision ID: d4e662a9926e
Revises: ca4c39594fff
Create Date: 2024-11-30 04:27:08.161561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e662a9926e'
down_revision = 'ca4c39594fff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('histories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('result', sa.ARRAY(sa.JSON()), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('histories', schema=None) as batch_op:
        batch_op.drop_column('result')

    # ### end Alembic commands ###