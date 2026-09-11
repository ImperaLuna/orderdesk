from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.ids import new_principal_id
from app.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, user_id: UUID) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def create(self, *, email: str, display_name: str) -> User:
        user = User(email=email, display_name=display_name)
        self.session.add(user)
        await self.session.flush()
        return user

    async def list(self, *, limit: int = 50) -> list[User]:
        stmt = select(User).order_by(User.created_at.desc()).limit(limit)
        return list((await self.session.execute(stmt)).scalars())

    async def get_random(self) -> User | None:
        """Random row via probe + index seek. ORDER BY RANDOM() is banned (ADR-0003)."""
        probe = new_principal_id()
        stmt = select(User).where(User.id >= probe).order_by(User.id).limit(1)
        row = (await self.session.execute(stmt)).scalar_one_or_none()
        if row is None:
            stmt = select(User).order_by(User.id).limit(1)
            row = (await self.session.execute(stmt)).scalar_one_or_none()
        return row
