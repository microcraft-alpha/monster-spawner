"""Mob service test cases."""

import uuid

import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from monster_spawner.api.v1.mobs import schemas
from monster_spawner.domain import exceptions
from monster_spawner.domain.database import transactions
from monster_spawner.domain.mob import repositories, services

pytestmark = pytest.mark.asyncio


def init_mob_service(database_session: AsyncSession) -> services.MobService:
    """Shortcut for initializing MobService."""
    return services.MobService(
        transaction=transactions.DatabaseTransaction(session=database_session),
        repository=repositories.MobRepository(session=database_session),
    )


async def test_mob_create(database_session: AsyncSession):
    """Test creating a mob."""
    mob_srv = init_mob_service(database_session)
    data_object = schemas.MobInSchema(name="Slime")
    mob = await mob_srv.create(data_object)

    assert mob.id is not None


async def test_mob_create_not_unique(database_session: AsyncSession):
    """Test creating a mob with a name that already exists."""
    mob_srv = init_mob_service(database_session)
    data_object = schemas.MobInSchema(name="Slime")
    await mob_srv.create(data_object)

    with pytest.raises(exceptions.AlreadyExistsError):
        await mob_srv.create(data_object)


async def test_mob_get(database_session: AsyncSession):
    """Test retrieving a mob."""
    mob_srv = init_mob_service(database_session)
    data_object = schemas.MobInSchema(name="Slime")
    mob = await mob_srv.create(data_object)

    retrieved_mob = await mob_srv.get(mob.id)

    assert retrieved_mob.id == mob.id
    assert retrieved_mob.name == mob.name


async def test_mob_get_not_existing(database_session: AsyncSession):
    """Test retrieving a mob that does not exist."""
    mob_srv = init_mob_service(database_session)

    with pytest.raises(exceptions.DoesNotExistError):
        await mob_srv.get(uuid.uuid4())


async def test_mob_collect(database_session: AsyncSession):
    """Test retrieving all the mobs."""
    mob_srv = init_mob_service(database_session)
    # Add 3 mobs to the database
    for i in range(3):
        data_object = schemas.MobInSchema(name=f"Slime {i}")
        await mob_srv.create(data_object)

    retrieved_mobs = await mob_srv.get_all()

    assert len(list(retrieved_mobs)) == 3


async def test_mob_collect_with_filter(database_session: AsyncSession):
    """Test retrieving all the mobs with a filter applied."""
    mob_srv = init_mob_service(database_session)
    # Add 3 mobs to the database
    for i in range(3):
        data_object = schemas.MobInSchema(name=f"Slime {i}")
        await mob_srv.create(data_object)

    retrieved_mobs = await mob_srv.get_all(name="Slime 1")
    retrieved_mobs = list(retrieved_mobs)

    assert len(retrieved_mobs) == 1
    assert retrieved_mobs[0].name == "Slime 1"
