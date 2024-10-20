"""add transaction model

Revision ID: e581a614cf6b
Revises: 0fde739396dc
Create Date: 2024-10-20 16:48:30.481025

"""
from typing import Union
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e581a614cf6b'
down_revision: str | None = '0fde739396dc'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('buyer_id', sa.Uuid(), nullable=False),
    sa.Column('seller_id', sa.Uuid(), nullable=False),
    sa.Column('stock_id', sa.Uuid(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['seller_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['stock_id'], ['stock.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    # ### end Alembic commands ###
