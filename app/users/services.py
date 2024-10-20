from app.core.security import get_password_hash, verify_password
from app.users.models import User
from app.users.schemas import UserInfo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


async def create_user(
        *, session: AsyncSession, user: UserInfo, username: str, password: str
) -> User:
    db_obj = User.model_validate(
        user,
        update={
            "hashed_password": get_password_hash(password),
            "username": username,
        },
    )

    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_user_by_username(*, session: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.username == username)
    users = await session.scalars(query)
    return users.first()


async def authenticate(
        *, session: AsyncSession, username: str, password: str
) -> User | None:
    user = await get_user_by_username(session=session, username=username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
