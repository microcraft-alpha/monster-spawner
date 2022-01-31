"""App handlers."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from structlog import get_logger

from monster_spawner.api import router
from monster_spawner.handlers import EXCEPTION_HANDLERS
from monster_spawner.settings import settings

logger = get_logger(__name__)


def create_application() -> FastAPI:
    """Create the FastAPI application.

    Returns:
        FastAPI: created app.
    """
    logger.info("Creating app...")
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url="/api/docs",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
    )
    app.include_router(router.api_router)
    app.exception_handlers = dict(EXCEPTION_HANDLERS)
    app.middleware_stack = app.build_middleware_stack()
    return app


app = create_application()
