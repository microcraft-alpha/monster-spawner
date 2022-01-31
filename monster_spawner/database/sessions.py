"""Database session helpers."""

from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from monster_spawner.settings import settings


def get_connection(
    database_url: str,
) -> tuple[AsyncEngine, Callable[..., AsyncSession]]:
    """Prepare a database connection.

    Args:
        database_url (str): database url.

    Returns:
        tuple[AsyncEngine, Callable[..., AsyncSession]]: async engine
            and session.
    """
    engine = create_async_engine(database_url)
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return engine, async_session


engine, async_session = get_connection(
    settings.DATABASE_URL + settings.DATABASE_NAME,
)


async def get_session():  # pragma: no cover
    """Create a new session.

    Yields:
        AsyncSession: database session.
    """
    async with async_session() as session:
        yield session
        await session.commit()
