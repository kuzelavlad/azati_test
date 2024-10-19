import uuid
from decimal import Decimal

from sqlmodel import SQLModel, Field, Relationship


class Order(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    stock_id: uuid.UUID = Field(foreign_key="stocks.id", nullable=False)
    order_type: str = Field(max_length=16, nullable=False)
    amount: int = Field(default=0, nullable=False)
    price: Decimal = Field(default=0, nullable=False)

    stocks: "Stocks" = Relationship(back_populates="orders")
