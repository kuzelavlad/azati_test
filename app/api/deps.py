from collections.abc import AsyncIterator
from typing import Annotated

from app.core.config import settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)


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
