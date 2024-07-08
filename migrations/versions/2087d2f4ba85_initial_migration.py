"""initial migration

Revision ID: 2087d2f4ba85
Revises: 
Create Date: 2024-06-28 09:23:21.909758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2087d2f4ba85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mechanics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('owners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(), nullable=True),
    sa.Column('chasis_no', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], name=op.f('fk_cars_owner_id_owners')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('owner_mechanics',
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('mechanic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanics.id'], name=op.f('fk_owner_mechanics_mechanic_id_mechanics')),
    sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], name=op.f('fk_owner_mechanics_owner_id_owners')),
    sa.PrimaryKeyConstraint('owner_id', 'mechanic_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('owner_mechanics')
    op.drop_table('cars')
    op.drop_table('owners')
    op.drop_table('mechanics')
    # ### end Alembic commands ###