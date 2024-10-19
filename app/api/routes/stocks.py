from fastapi import APIRouter

from datetime import datetime

from sqlmodel import select

from app.api.deps import SessionDep
from app.stocks.models import Stock
from app.stocks.schemas import StockCreate
router = APIRouter()


@router.post("/create-stock")
async def create_stock(
        session: SessionDep,
        create_data: StockCreate
):
    new_stock = Stock(
        title=create_data.title,
        total_shares=create_data.total_shares,
        created_at=datetime.now()
    )

    session.add(new_stock)
    await session.commit()
    await session.refresh(new_stock)
    return new_stock


@router.get("/", response_model=list[Stock])
async def get_stocks(session: SessionDep):
    result = await session.execute(select(Stock))
    stocks = result.scalars().all()
    return stocks
