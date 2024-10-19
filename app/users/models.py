import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(max_length=50, nullable=False)
    last_name: str = Field(max_length=50, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
    is_blocked: bool = False
    is_superuser: bool = False
    username: str = Field(max_length=64, nullable=True, default=None)
    password: str = Field(max_length=64, nullable=True, default=None)
    auth_token: str = Field(max_length=64, nullable=True, default=None)
    