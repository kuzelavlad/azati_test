"""update transaction model

Revision ID: e9f1c780b221
Revises: e581a614cf6b
Create Date: 2024-10-20 16:58:08.490124

"""
from typing import Union
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9f1c780b221'
down_revision: str | None = 'e581a614cf6b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('buy_order_id', sa.Uuid(), nullable=False))
    op.add_column('transaction', sa.Column('sell_order_id', sa.Uuid(), nullable=False))
    op.add_column('transaction', sa.Column('amount_of_shares', sa.Integer(), nullable=False))
    op.add_column('transaction', sa.Column('price_per_share', sa.Numeric(), nullable=False))
    op.add_column('transaction', sa.Column('total_price', sa.Numeric(), nullable=False))
    op.drop_constraint('transaction_buyer_id_fkey', 'transaction', type_='foreignkey')
    op.drop_constraint('transaction_seller_id_fkey', 'transaction', type_='foreignkey')
    op.create_foreign_key(None, 'transaction', 'order', ['buy_order_id'], ['id'])
    op.create_foreign_key(None, 'transaction', 'order', ['sell_order_id'], ['id'])
    op.drop_column('transaction', 'seller_id')
    op.drop_column('transaction', 'amount')
    op.drop_column('transaction', 'price')
    op.drop_column('transaction', 'buyer_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('buyer_id', sa.UUID(), autoincrement=False, nullable=False))
    op.add_column('transaction', sa.Column('price', sa.NUMERIC(), autoincrement=False, nullable=False))
    op.add_column('transaction', sa.Column('amount', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('transaction', sa.Column('seller_id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.create_foreign_key('transaction_seller_id_fkey', 'transaction', 'user', ['seller_id'], ['id'])
    op.create_foreign_key('transaction_buyer_id_fkey', 'transaction', 'user', ['buyer_id'], ['id'])
    op.drop_column('transaction', 'total_price')
    op.drop_column('transaction', 'price_per_share')
    op.drop_column('transaction', 'amount_of_shares')
    op.drop_column('transaction', 'sell_order_id')
    op.drop_column('transaction', 'buy_order_id')
    # ### end Alembic commands ###
