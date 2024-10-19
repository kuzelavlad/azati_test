import uuid
from datetime import datetime
from decimal import Decimal

from sqlmodel import SQLModel, Field


class Order(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    stock_id: uuid.UUID = Field(foreign_key="stock.id", nullable=False)
    order_type: str = Field(max_length=16, nullable=False)
    amount_of_shares: int = Field(default=0, nullable=False)
    price_per_share: Decimal = Field(default=0, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
