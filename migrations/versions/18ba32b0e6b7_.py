"""empty message

Revision ID: 18ba32b0e6b7
Revises: 28ee22c17aae
Create Date: 2014-11-17 22:15:03.835000

"""

# revision identifiers, used by Alembic.
revision = '18ba32b0e6b7'
down_revision = '28ee22c17aae'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('match_player', sa.Column('position', sa.Enum('GK', 'DF', 'MF', 'FW'), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('match_player', 'position')
    ### end Alembic commands ###
