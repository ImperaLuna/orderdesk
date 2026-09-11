from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Order, OrderEvent, OrderStatus


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, order_id: UUID) -> Order | None:
        stmt = select(Order).where(Order.id == order_id).options(selectinload(Order.events))
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def create(self, *, user_id: UUID, currency: str, total_cents: int) -> Order:
        order = Order(user_id=user_id, currency=currency, total_cents=total_cents)
        order.events.append(OrderEvent(kind="created", payload={"total_cents": total_cents}))
        self.session.add(order)
        await self.session.flush()
        return order

    async def set_status(self, order: Order, status: OrderStatus) -> Order:
        previous = order.status
        order.status = status
        order.events.append(
            OrderEvent(kind="status_changed", payload={"from": previous, "to": status})
        )
        await self.session.flush()
        return order

    async def page(self, *, after: UUID | None, limit: int) -> list[Order]:
        """Keyset pagination on the primary key."""
        stmt = select(Order).order_by(Order.id).limit(limit)
        if after is not None:
            stmt = stmt.where(Order.id > after)
        return list((await self.session.execute(stmt)).scalars())

    async def list_for_user(self, user_id: UUID, *, limit: int = 50) -> list[Order]:
        stmt = select(Order).where(Order.user_id == user_id).order_by(Order.id.desc()).limit(limit)
        return list((await self.session.execute(stmt)).scalars())
