"""empty message

Revision ID: b42507b2ae51
Revises: bc7f4ffc1fa8
Create Date: 2020-11-23 22:27:06.221560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b42507b2ae51'
down_revision = 'bc7f4ffc1fa8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dishes', sa.Column('cooking_time', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dishes', 'cooking_time')
    # ### end Alembic commands ###
