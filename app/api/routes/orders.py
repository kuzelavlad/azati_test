import uuid
from datetime import datetime

from app.api.deps import SessionDep
from app.orders.models import Order
from app.orders.schemas import OrderCreate, OrderResponse
from app.orders.services import match_orders
from app.stocks.models import Stock
from fastapi import APIRouter, HTTPException
from sqlmodel import select

router = APIRouter()


@router.post("/create-order")
async def create_order(session: SessionDep, create_data: OrderCreate):
    new_order = Order(
        user_id=create_data.user_id,
        stock_id=create_data.stock_id,
        order_type=create_data.order_type,
        amount_of_shares=create_data.amount_of_shares,
        price_per_share=create_data.price_per_share,
        created_at=datetime.now(),
    )

    session.add(new_order)

    await match_orders(session, new_order)

    await session.commit()
    await session.refresh(new_order)

    return new_order


@router.get("/{stock_id}", response_model=list[OrderResponse])
async def get_orders(session: SessionDep, stock_id: uuid.UUID):
    stock = await session.get(Stock, stock_id)
    if stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    result = await session.execute(select(Order).where(Order.stock_id == stock_id))
    orders = result.scalars().all()

    orders_response = [
        OrderResponse(
            user_id=order.user_id,
            order_type=order.order_type,
            amount_of_shares=order.amount_of_shares,
            price_per_share=order.price_per_share,
            created_at=order.created_at,
        )
        for order in orders
    ]

    return orders_response
