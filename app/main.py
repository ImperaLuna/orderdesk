from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, Response

from app.api.v1.router import router
from app.core.config import get_settings
from app.core.ids import new_principal_id
from app.core.logging import configure_logging
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    structlog.get_logger().info("startup", env=settings.app_env)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="orderdesk", version="0.1.0", lifespan=lifespan)

    @app.middleware("http")
    async def request_id(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        rid = request.headers.get("x-request-id") or str(new_principal_id())
        structlog.contextvars.bind_contextvars(request_id=rid)
        response = await call_next(request)
        response.headers["x-request-id"] = rid
        structlog.contextvars.unbind_contextvars("request_id")
        return response

    app.include_router(router)
    return app


app = create_app()
