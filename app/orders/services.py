from datetime import datetime
from sqlmodel import select

from app.orders.models import Order
from app.api.deps import SessionDep
from app.transactions.models import Transaction


async def match_orders(session: SessionDep, new_order: Order):
    stock_id = new_order.stock_id

    if new_order.order_type == "buy":
        sell_orders = await session.execute(
            select(Order)
            .where(Order.stock_id == stock_id)
            .where(Order.order_type == "sell")
            .where(Order.price_per_share <= new_order.price_per_share)
            .order_by(Order.price_per_share, Order.created_at)
        )
        sell_orders = sell_orders.scalars().all()

        for sell_order in sell_orders:
            if new_order.amount_of_shares == 0:
                break

            matched_shares = min(new_order.amount_of_shares, sell_order.amount_of_shares)
            total_price = matched_shares * sell_order.price_per_share

            transaction = Transaction(
                stock_id=stock_id,
                buy_order_id=new_order.id,
                sell_order_id=sell_order.id,
                amount_of_shares=matched_shares,
                price_per_share=sell_order.price_per_share,
                total_price=total_price,
                created_at=datetime.now()
            )
            session.add(transaction)

            new_order.amount_of_shares -= matched_shares
            sell_order.amount_of_shares -= matched_shares

            if sell_order.amount_of_shares == 0:
                sell_order.amount_of_shares = 0

    elif new_order.order_type == "sell":
        buy_orders = await session.execute(
            select(Order)
            .where(Order.stock_id == stock_id)
            .where(Order.order_type == "buy")
            .where(Order.price_per_share >= new_order.price_per_share)
            .order_by(Order.price_per_share.desc(), Order.created_at)
        )
        buy_orders = buy_orders.scalars().all()

        for buy_order in buy_orders:
            if new_order.amount_of_shares == 0:
                break

            matched_shares = min(new_order.amount_of_shares, buy_order.amount_of_shares)
            total_price = matched_shares * buy_order.price_per_share

            transaction = Transaction(
                stock_id=stock_id,
                buy_order_id=buy_order.id,
                sell_order_id=new_order.id,
                amount_of_shares=matched_shares,
                price_per_share=buy_order.price_per_share,
                total_price=total_price,
                created_at=datetime.now()
            )
            session.add(transaction)

            new_order.amount_of_shares -= matched_shares
            buy_order.amount_of_shares -= matched_shares

            if buy_order.amount_of_shares == 0:
                buy_order.amount_of_shares = 0

    await session.commit()
