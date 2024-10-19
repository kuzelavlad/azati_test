from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class UserCreate(SQLModel):
    first_name: str
    last_name: Optional[str]
    is_active: bool
    is_blocked: bool
    is_superuser: bool
    created_at: datetime


class UserInfo(SQLModel):
    first_name: str
    last_name: Optional[str]
    is_active: bool
    created_at: datetime
