"""added column to car

Revision ID: 40dbe76abe4c
Revises: 16365690b1a2
Create Date: 2024-07-03 10:18:44.886168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40dbe76abe4c'
down_revision = '16365690b1a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.add_column(sa.Column('purchase', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('sell', sa.Integer(), nullable=True))
        batch_op.drop_column('fleet_no')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cars', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fleet_no', sa.INTEGER(), nullable=True))
        batch_op.drop_column('sell')
        batch_op.drop_column('purchase')

    # ### end Alembic commands ###
