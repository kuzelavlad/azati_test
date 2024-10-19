from sqlmodel import SQLModel
from datetime import datetime

from typing import Optional


class StockCreate(SQLModel):
    title: str
    total_shares: int
    created_at: Optional[datetime] = None
