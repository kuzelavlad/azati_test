import uuid
from datetime import timedelta

from fastapi import APIRouter, HTTPException

from sqlmodel import select

from app.api.deps import SessionDep, CurrentUser
from app.users.models import User
from app.users.schemas import UserCreate, Token, UserLogin, UserInfo
from app.core.security import get_password_hash
from app.users import services
from app.core import security
from app.core.config import settings
from app.orders.schemas import OrderResponse
from app.orders.models import Order

router = APIRouter()


@router.post("/register")
async def register_user(user_data: UserCreate, session: SessionDep):
    existing_user = await session.execute(select(User).where(User.username == user_data.username))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_active=True
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"msg": "User registered successfully"}


@router.post("/login", response_model=Token)
async def login_user(session: SessionDep, data: UserLogin) -> Token:
    user = await services.authenticate(
        session=session, username=data.username, password=data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")  # Исправлено

    if not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")

    if user.is_blocked:
        raise HTTPException(status_code=403, detail="User is blocked")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=str(user.id), expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type=settings.TOKEN_TYPE)


@router.get("/me", response_model=UserInfo)
async def get_user_info(current_user: CurrentUser):
    return UserInfo(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.get("/me/orders", response_model=list[OrderResponse])
async def get_my_orders(session: SessionDep, current_user: CurrentUser):
    orders = await session.execute(
        select(Order).where(Order.user_id == current_user.id)
    )

    return orders.scalars().all()


@router.delete("/me/orders/{order_id}")
async def cancel_order(session: SessionDep,order_id: uuid.UUID, current_user: CurrentUser):
    query = select(Order).where(Order.id == order_id, Order.user_id == current_user.id)
    order = await session.execute(query)
    order = order.scalars().first()

    if not order:
        raise HTTPException(status_code=404,
                            detail="Order not found or you do not have permission to cancel this order")

    await session.delete(order)
    await session.commit()

    return {"msg": "Order cancelled successfully"}
