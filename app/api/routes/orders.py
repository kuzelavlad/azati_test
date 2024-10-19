from fastapi import APIRouter

from datetime import datetime

from app.api.deps import SessionDep
from app.orders.models import Order
from app.orders.schemas import OrderCreate

router = APIRouter()


@router.post("/create-order")
async def create_order(
        session: SessionDep,
        create_data: OrderCreate
):
    new_order = Order(
        user_id=create_data.user_id,
        stock_id=create_data.stock_id,
        order_type=create_data.order_type,
        amount_of_shares=create_data.amount_of_shares,
        price_per_share=create_data.price_per_share,
        created_at=datetime.now()

    )
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    return new_order
