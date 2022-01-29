"""Mob sqlalchemy repository test cases."""

import uuid

import pytest
from sqlalchemy import exc as sql_exceptions
from sqlalchemy.ext.asyncio.session import AsyncSession

from monster_spawner.api.v1.mobs import schemas
from monster_spawner.domain import exceptions as domain_exceptions
from monster_spawner.domain.mob import repositories

pytestmark = pytest.mark.asyncio


async def test_mob_create(database_session: AsyncSession):
    """Test creating a mob."""
    repo = repositories.MobRepository(session=database_session)
    data_object = schemas.MobInSchema(name="Skeleton")
    mob = await repo.create(data_object)

    assert mob.id is not None


async def test_mob_create_not_unique(database_session: AsyncSession):
    """Test creating a mob with a name that already exists."""
    repo = repositories.MobRepository(session=database_session)
    data_object = schemas.MobInSchema(name="Skeleton")
    await repo.create(data_object)

    with pytest.raises(sql_exceptions.IntegrityError):
        await repo.create(data_object)


async def test_mob_get(database_session: AsyncSession):
    """Test retrieving a mob."""
    repo = repositories.MobRepository(session=database_session)
    data_object = schemas.MobInSchema(name="Skeleton")
    mob = await repo.create(data_object)

    retrieved_mob = await repo.get_by_id(mob.id)

    assert retrieved_mob.id == mob.id
    assert retrieved_mob.name == mob.name


async def test_mob_get_not_existing(database_session: AsyncSession):
    """Test retrieving a mob that does not exist."""
    repo = repositories.MobRepository(session=database_session)

    with pytest.raises(domain_exceptions.DoesNotExistError):
        await repo.get_by_id(uuid.uuid4())


async def test_mob_collect(database_session: AsyncSession):
    """Test retrieving all the mobs."""
    repo = repositories.MobRepository(session=database_session)
    # Add 3 mobs to the database
    for i in range(3):
        data_object = schemas.MobInSchema(name=f"Skeleton {i}")
        await repo.create(data_object)

    retrieved_mobs = await repo.collect()

    assert len(list(retrieved_mobs)) == 3


async def test_mob_collect_with_filter(database_session: AsyncSession):
    """Test retrieving all the mobs with a filter applied."""
    repo = repositories.MobRepository(session=database_session)
    # Add 3 mobs to the database
    for i in range(3):
        data_object = schemas.MobInSchema(name=f"Skeleton {i}")
        await repo.create(data_object)

    retrieved_mobs = await repo.collect(name="Skeleton 1")
    retrieved_mobs = list(retrieved_mobs)

    assert len(retrieved_mobs) == 1
    assert retrieved_mobs[0].name == "Skeleton 1"
