"""Seed a local database with users and orders.

uv run python -m scripts.seed
"""

import asyncio
import random

from app.db.session import SessionLocal
from app.repositories.order import OrderRepository
from app.repositories.user import UserRepository

USERS = 50
ORDERS_PER_USER = 20


async def main() -> None:
    rng = random.Random(42)
    async with SessionLocal() as session:
        users = UserRepository(session)
        orders = OrderRepository(session)
        for i in range(USERS):
            user = await users.create(email=f"user{i}@example.com", display_name=f"User {i}")
            for _ in range(ORDERS_PER_USER):
                await orders.create(
                    user_id=user.id,
                    currency=rng.choice(["USD", "EUR", "GBP"]),
                    total_cents=rng.randint(500, 250_000),
                )
        await session.commit()
    print(f"seeded {USERS} users, {USERS * ORDERS_PER_USER} orders")


if __name__ == "__main__":
    asyncio.run(main())
