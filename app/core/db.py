from app.core.config import settings
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.replace("+asyncpg", ""), poolclass=StaticPool)
