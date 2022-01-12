"""Database session helpers."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from monster_spawner.settings import settings

engine = create_async_engine(settings.DATABASE_URL)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    """Create a new session.

    Yields:
        AsyncSession: database session.
    """
    async with async_session() as session:
        yield session
        await session.commit()
