import uuid
from decimal import Decimal
from datetime import datetime

from sqlmodel import SQLModel


class OrderCreate(SQLModel):
    user_id: uuid.UUID
    stock_id: uuid.UUID
    order_type: str
    amount_of_shares: int
    price_per_share: Decimal


class OrderResponse(SQLModel):
    user_id: uuid.UUID
    order_type: str
    amount_of_shares: int
    price_per_share: Decimal
    created_at: datetime
