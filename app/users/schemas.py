from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class TokenPayload(SQLModel):
    sub: str | None = None


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(SQLModel):
    username: str
    password: str
    first_name: str
    last_name: str


class UserLogin(SQLModel):
    username: str
    password: str


class UserInfo(SQLModel):
    first_name: str
    last_name: Optional[str]
    is_active: bool
    created_at: datetime
