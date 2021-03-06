"""empty message

Revision ID: 5429cb33ab02
Revises: 45a1e07f043a
Create Date: 2014-11-06 15:42:17.519000

"""

# revision identifiers, used by Alembic.
revision = '5429cb33ab02'
down_revision = '45a1e07f043a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('team', 'yellow_card')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('team', sa.Column('yellow_card', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    ### end Alembic commands ###
