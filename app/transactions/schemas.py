import uuid
from decimal import Decimal

from sqlmodel import SQLModel


class TransactionResponse(SQLModel):
    id: uuid.UUID
    stock_id: uuid.UUID
    seller_id: uuid.UUID
    buyer_id: uuid.UUID
    amount_of_shares: int
    price_per_share: Decimal
    total_price: Decimal
