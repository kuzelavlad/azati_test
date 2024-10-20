import uuid
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter
from sqlmodel import Field, SQLModel

router = APIRouter()


class Transaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    buy_order_id: uuid.UUID = Field(foreign_key="order.id", nullable=False)
    sell_order_id: uuid.UUID = Field(foreign_key="order.id", nullable=False)
    stock_id: uuid.UUID = Field(foreign_key="stock.id", nullable=False)
    amount_of_shares: int = Field(default=0, nullable=False)
    price_per_share: Decimal = Field(default=0, nullable=False)
    total_price: Decimal = Field(default=0, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
