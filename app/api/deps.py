import jwt

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.users.models import User
from app.core import security
from app.core.config import settings
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.users.schemas import TokenPayload

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


def async_session_maker():
    return async_sessionmaker(async_engine, expire_on_commit=False)()


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


def get_sync_session():
    Session = sessionmaker(engine)  # noqa
    sync_session = Session()
    return sync_session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(session: SessionDep, token: TokenDep) -> type[User]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
