"""App handlers."""

from fastapi import FastAPI
from structlog import get_logger

from monster_spawner.api import router
from monster_spawner.settings import settings

log = get_logger()


def create_application() -> FastAPI:
    """Create the FastAPI application.

    Returns:
        FastAPI: created app.
    """
    log.info("Creating app...")
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url="/api/docs",
    )
    app.include_router(router.api_router)
    return app


app = create_application()
