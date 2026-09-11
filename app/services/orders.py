from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order, OrderStatus
from app.repositories.order import OrderRepository
from app.repositories.user import UserRepository


class OrderNotFound(LookupError):
    pass


class UserNotFound(LookupError):
    pass


class InvalidTransition(ValueError):
    pass


_ALLOWED: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.pending: {OrderStatus.paid, OrderStatus.cancelled},
    OrderStatus.paid: {OrderStatus.shipped, OrderStatus.cancelled},
    OrderStatus.shipped: set(),
    OrderStatus.cancelled: set(),
}


class OrderService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.orders = OrderRepository(session)
        self.users = UserRepository(session)

    async def place(self, *, user_id: UUID, currency: str, total_cents: int) -> Order:
        if await self.users.get(user_id) is None:
            raise UserNotFound(user_id)
        order = await self.orders.create(
            user_id=user_id, currency=currency.upper(), total_cents=total_cents
        )
        await self.session.commit()
        return order

    async def transition(self, order_id: UUID, status: OrderStatus) -> Order:
        order = await self.orders.get(order_id)
        if order is None:
            raise OrderNotFound(order_id)
        if status not in _ALLOWED[order.status]:
            raise InvalidTransition(f"{order.status} -> {status}")
        order = await self.orders.set_status(order, status)
        await self.session.commit()
        return order
