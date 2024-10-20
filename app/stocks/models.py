import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel


class Stock(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=64, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
