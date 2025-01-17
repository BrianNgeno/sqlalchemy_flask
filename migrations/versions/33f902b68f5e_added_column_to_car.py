"""added column to car

Revision ID: 33f902b68f5e
Revises: 40dbe76abe4c
Create Date: 2024-07-03 10:55:32.378535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33f902b68f5e'
down_revision = '40dbe76abe4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.drop_column('sell')
        batch_op.drop_column('purchase')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.add_column(sa.Column('purchase', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('sell', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
