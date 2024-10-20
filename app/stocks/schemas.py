from datetime import datetime

from sqlmodel import SQLModel


class StockCreate(SQLModel):
    title: str
    total_shares: int
    created_at: datetime | None = None
