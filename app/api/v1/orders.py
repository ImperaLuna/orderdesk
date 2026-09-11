from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import OrderRepo, Orders
from app.models import OrderStatus
from app.schemas.order import OrderCreate, OrderEventRead, OrderPage, OrderRead
from app.services.orders import InvalidTransition, OrderNotFound, UserNotFound

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=OrderPage)
async def list_orders(
    repo: OrderRepo,
    after: UUID | None = None,
    limit: int = Query(50, ge=1, le=200),
) -> OrderPage:
    rows = await repo.page(after=after, limit=limit)
    items = [OrderRead.model_validate(o) for o in rows]
    next_cursor = items[-1].id if len(items) == limit else None
    return OrderPage(items=items, next_cursor=next_cursor)


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def place_order(body: OrderCreate, svc: Orders) -> OrderRead:
    try:
        order = await svc.place(
            user_id=body.user_id, currency=body.currency, total_cents=body.total_cents
        )
    except UserNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found") from e
    return OrderRead.model_validate(order)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: UUID, repo: OrderRepo) -> OrderRead:
    order = await repo.get(order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "order not found")
    return OrderRead.model_validate(order)


@router.get("/{order_id}/events", response_model=list[OrderEventRead])
async def order_events(order_id: UUID, repo: OrderRepo) -> list[OrderEventRead]:
    order = await repo.get(order_id)
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "order not found")
    return [OrderEventRead.model_validate(e) for e in order.events]


@router.post("/{order_id}/status", response_model=OrderRead)
async def set_status(order_id: UUID, new_status: OrderStatus, svc: Orders) -> OrderRead:
    try:
        order = await svc.transition(order_id, new_status)
    except OrderNotFound as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "order not found") from e
    except InvalidTransition as e:
        raise HTTPException(status.HTTP_409_CONFLICT, str(e)) from e
    return OrderRead.model_validate(order)
