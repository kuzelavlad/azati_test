"""delete total_shares field in stock model

Revision ID: 00af208bdbda
Revises: e9f1c780b221
Create Date: 2024-10-20 17:54:30.046969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00af208bdbda'
down_revision: Union[str, None] = 'e9f1c780b221'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stock', 'total_shares')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stock', sa.Column('total_shares', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
