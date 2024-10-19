import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.users.models import User
from app.users.schemas import UserCreate, UserInfo

router = APIRouter()


@router.post("/create-user")
async def create_user(
        session: SessionDep,
        create_data: UserCreate
):
    new_user = User(
        first_name=create_data.first_name,
        last_name=create_data.last_name,
        is_active=create_data.is_active,
        is_superuser=create_data.is_superuser,
        is_blocked=create_data.is_blocked,
        created_at=datetime.now()
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get("/", response_model=list[User])
async def get_users(
        session: SessionDep,
):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserInfo)
async def get_user_info(
        session: SessionDep,
        user_id: uuid.UUID
):
    result = await session.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserInfo(
        first_name=user.first_name,
        last_name=user.last_name,
        is_active=user.is_active,
        created_at=user.created_at,
    )
