from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.repositories.order import OrderRepository
from app.repositories.user import UserRepository
from app.services.orders import OrderService


async def db(session: Annotated[AsyncSession, Depends(get_session)]) -> AsyncIterator[AsyncSession]:
    yield session


DB = Annotated[AsyncSession, Depends(db)]


def user_repo(session: DB) -> UserRepository:
    return UserRepository(session)


def order_repo(session: DB) -> OrderRepository:
    return OrderRepository(session)


def order_service(session: DB) -> OrderService:
    return OrderService(session)


UserRepo = Annotated[UserRepository, Depends(user_repo)]
OrderRepo = Annotated[OrderRepository, Depends(order_repo)]
Orders = Annotated[OrderService, Depends(order_service)]
