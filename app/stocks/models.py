import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Stocks(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=64, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)

    orders: list["Order"] = Relationship(back_populates="stocks")
