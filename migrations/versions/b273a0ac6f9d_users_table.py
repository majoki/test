"""users table

Revision ID: b273a0ac6f9d
Revises: 5d46d1ba8776
Create Date: 2020-02-12 22:20:42.444649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b273a0ac6f9d'
down_revision = '5d46d1ba8776'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###
