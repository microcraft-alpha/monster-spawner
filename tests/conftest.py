"""Tests fixtures."""

import asyncio
import typing as T  # noqa: WPS111,N812

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from monster_spawner.database import base, sessions
from monster_spawner.main import app as base_app
from monster_spawner.settings import settings


@pytest.fixture(scope="session")
def event_loop() -> T.Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def database_session() -> T.AsyncGenerator:
    """Prepare a test database session."""
    engine, async_session = sessions.get_connection(settings.DATABASE_URL)
    async with engine.begin() as connection:
        await connection.run_sync(base.Model.metadata.drop_all)
        await connection.run_sync(base.Model.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture()
def test_app(database_session: AsyncSession) -> FastAPI:
    """Create a test FastAPI application with overridden dependencies."""

    async def override_get_db():
        return database_session

    base_app.dependency_overrides[sessions.get_session] = override_get_db
    return base_app


@pytest_asyncio.fixture()
async def async_client(test_app: FastAPI) -> T.AsyncGenerator:
    """Create an instance of the HTTP client."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client
