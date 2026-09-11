from fastapi import APIRouter
from sqlalchemy import text

from app.api.deps import DB

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/readyz")
async def readyz(session: DB) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ready"}
