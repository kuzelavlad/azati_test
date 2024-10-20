from app.api.deps import SessionDep
from app.transactions.models import Transaction
from app.transactions.schemas import TransactionResponse
from fastapi import APIRouter
from sqlmodel import select

router = APIRouter()


@router.get("/", response_model=list[TransactionResponse])
async def get_transactions(session: SessionDep):
    result = await session.execute(select(Transaction))
    transactions = result.scalars().all()
    transaction_responses = []
    for transaction in transactions:
        transaction_responses.append(
            TransactionResponse(
                id=transaction.id,
                stock_id=transaction.stock_id,
                seller_id=transaction.sell_order_id,
                buyer_id=transaction.buy_order_id,
                amount_of_shares=transaction.amount_of_shares,
                price_per_share=transaction.price_per_share,
                total_price=transaction.total_price,
            )
        )

    return transaction_responses
