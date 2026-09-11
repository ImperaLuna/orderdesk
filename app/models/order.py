import enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import JSON, Enum, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.ids import new_record_id
from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class OrderStatus(enum.StrEnum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    cancelled = "cancelled"


class Order(TimestampMixin, Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=new_record_id)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"), default=OrderStatus.pending, nullable=False
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    total_cents: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped[User] = relationship(back_populates="orders")
    events: Mapped[list[OrderEvent]] = relationship(
        back_populates="order", cascade="all, delete-orphan", order_by="OrderEvent.id"
    )


class OrderEvent(Base):
    __tablename__ = "order_events"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=new_record_id)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(40), nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(JSON, default=dict, nullable=False)

    order: Mapped[Order] = relationship(back_populates="events")
