from app.api.routes import auth, orders, stocks, transactions, users
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["transactions"]
)
