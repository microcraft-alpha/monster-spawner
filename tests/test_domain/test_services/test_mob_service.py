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
    data_object = schemas.MobCreateSchema(name="Slime")
    mob = await mob_srv.create(data_object)

    assert mob.id is not None


async def test_mob_create_not_unique(database_session: AsyncSession):
    """Test creating a mob with a name that already exists."""
    mob_srv = init_mob_service(database_session)
    data_object = schemas.MobCreateSchema(name="Slime")
    await mob_srv.create(data_object)

    with pytest.raises(exceptions.AlreadyExistsError):
        await mob_srv.create(data_object)


async def test_mob_get(database_session: AsyncSession):
    """Test retrieving a mob."""
    mob_srv = init_mob_service(database_session)
    data_object = schemas.MobCreateSchema(name="Slime")
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
        data_object = schemas.MobCreateSchema(name=f"Slime {i}")
        await mob_srv.create(data_object)

    retrieved_mobs = await mob_srv.get_all()

    assert len(list(retrieved_mobs)) == 3


async def test_mob_collect_with_filter(database_session: AsyncSession):
    """Test retrieving all the mobs with a filter applied."""
    mob_srv = init_mob_service(database_session)
    # Add 3 mobs to the database
    for i in range(3):
        data_object = schemas.MobCreateSchema(name=f"Slime {i}")
        await mob_srv.create(data_object)

    retrieved_mobs = await mob_srv.get_all(name="Slime 1")
    retrieved_mobs = list(retrieved_mobs)

    assert len(retrieved_mobs) == 1
    assert retrieved_mobs[0].name == "Slime 1"


async def test_mob_delete(database_session: AsyncSession):
    """Test deleting a mob."""
    mob_srv = init_mob_service(database_session)
    data_object = schemas.MobCreateSchema(name="Slime")
    mob = await mob_srv.create(data_object)

    await mob_srv.delete(mob.id)

    with pytest.raises(exceptions.DoesNotExistError):
        await mob_srv.get(mob.id)


async def test_mob_delete_not_existing(database_session: AsyncSession):
    """Test deleting a mob that does not exist."""
    mob_srv = init_mob_service(database_session)

    with pytest.raises(exceptions.DoesNotExistError):
        await mob_srv.delete(uuid.uuid4())


async def test_mob_update(database_session: AsyncSession):
    """Test updating a mob."""
    mob_srv = init_mob_service(database_session)
    data_object = schemas.MobCreateSchema(name="Slime")
    mob = await mob_srv.create(data_object)

    data_object = schemas.MobUpdateSchema(name="Slime Updated")
    updated_mob = await mob_srv.update(mob.id, data_object)

    assert updated_mob.name == "Slime Updated"


async def test_mob_update_not_existing(database_session: AsyncSession):
    """Test updating a mob that does not exist."""
    mob_srv = init_mob_service(database_session)
    data_object = schemas.MobUpdateSchema(name="Slime")

    with pytest.raises(exceptions.DoesNotExistError):
        await mob_srv.update(uuid.uuid4(), data_object)


async def test_mob_update_not_unique(database_session: AsyncSession):
    """Test updating a mob that already exists."""
    mob_srv = init_mob_service(database_session)
    slime_object = schemas.MobCreateSchema(name="Slime")
    skeleton_object = schemas.MobCreateSchema(name="Skeleton")
    slime = await mob_srv.create(slime_object)
    await mob_srv.create(skeleton_object)

    data_object = schemas.MobUpdateSchema(name="Skeleton")
    with pytest.raises(exceptions.AlreadyExistsError):
        await mob_srv.update(slime.id, data_object)
