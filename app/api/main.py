from app.api.routes import users, stocks, orders
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
