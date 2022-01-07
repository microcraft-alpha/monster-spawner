"""App handlers."""

from fastapi import FastAPI
from structlog import get_logger

from monster_spawner.settings import settings

log = get_logger()


def create_application() -> FastAPI:
    """Create the FastAPI application and add the GraphQL endpoint.

    Returns:
        FastAPI: created FastAPI application.
    """
    log.info("Creating app...")
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )
    return app


app = create_application()


@app.on_event("startup")
async def startup_event() -> None:
    """Log the startup."""
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Log the shutdown."""
    log.info("Shutting down...")
