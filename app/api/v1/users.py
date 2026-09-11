from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.deps import DB, UserRepo
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
async def list_users(repo: UserRepo, limit: int = 50) -> list[UserRead]:
    return [UserRead.model_validate(u) for u in await repo.list(limit=limit)]


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreate, repo: UserRepo, session: DB) -> UserRead:
    if await repo.get_by_email(body.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "email already registered")
    user = await repo.create(email=body.email, display_name=body.display_name)
    await session.commit()
    return UserRead.model_validate(user)


@router.get("/random", response_model=UserRead)
async def random_user(repo: UserRepo) -> UserRead:
    """Used by the ops dashboard 'spotlight' widget."""
    user = await repo.get_random()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no users")
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, repo: UserRepo) -> UserRead:
    user = await repo.get(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return UserRead.model_validate(user)
