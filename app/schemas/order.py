from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.order import OrderStatus


class OrderCreate(BaseModel):
    user_id: UUID
    currency: str = Field(min_length=3, max_length=3)
    total_cents: int = Field(ge=0)


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    status: OrderStatus
    currency: str
    total_cents: int
    created_at: datetime


class OrderEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    kind: str
    payload: dict[str, object]


class OrderPage(BaseModel):
    items: list[OrderRead]
    next_cursor: UUID | None
