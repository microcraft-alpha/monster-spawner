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
    data_object = schemas.MobCreateSchema(name="Skeleton")
    mob = await repo.create(data_object)

    assert mob.id is not None


async def test_mob_create_not_unique(database_session: AsyncSession):
    """Test creating a mob with a name that already exists."""
    repo = repositories.MobRepository(session=database_session)
    data_object = schemas.MobCreateSchema(name="Skeleton")
    await repo.create(data_object)

    with pytest.raises(sql_exceptions.IntegrityError):
        await repo.create(data_object)


async def test_mob_get(database_session: AsyncSession):
    """Test retrieving a mob."""
    repo = repositories.MobRepository(session=database_session)
    data_object = schemas.MobCreateSchema(name="Skeleton")
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
        data_object = schemas.MobCreateSchema(name=f"Skeleton {i}")
        await repo.create(data_object)

    retrieved_mobs = await repo.collect()

    assert len(list(retrieved_mobs)) == 3


async def test_mob_collect_with_filter(database_session: AsyncSession):
    """Test retrieving all the mobs with a filter applied."""
    repo = repositories.MobRepository(session=database_session)
    # Add 3 mobs to the database
    for i in range(3):
        data_object = schemas.MobCreateSchema(name=f"Skeleton {i}")
        await repo.create(data_object)

    retrieved_mobs = await repo.collect(name="Skeleton 1")
    retrieved_mobs = list(retrieved_mobs)

    assert len(retrieved_mobs) == 1
    assert retrieved_mobs[0].name == "Skeleton 1"


async def test_mob_delete(database_session: AsyncSession):
    """Test deleting a mob."""
    repo = repositories.MobRepository(session=database_session)
    data_object = schemas.MobCreateSchema(name="Skeleton")
    mob = await repo.create(data_object)

    await repo.delete(mob.id)

    with pytest.raises(domain_exceptions.DoesNotExistError):
        await repo.get_by_id(mob.id)


async def test_mob_delete_not_existing(database_session: AsyncSession):
    """Test deleting a mob that does not exist."""
    repo = repositories.MobRepository(session=database_session)

    with pytest.raises(domain_exceptions.DoesNotExistError):
        await repo.delete(uuid.uuid4())


async def test_mob_update(database_session: AsyncSession):
    """Test updating a mob."""
    repo = repositories.MobRepository(session=database_session)
    data_object = schemas.MobCreateSchema(name="Skeleton")
    mob = await repo.create(data_object)

    await repo.update(mob.id, schemas.MobUpdateSchema(name="Skeleton 2"))

    updated_mob = await repo.get_by_id(mob.id)

    assert updated_mob.name == "Skeleton 2"


async def test_mob_update_not_unique_name(database_session: AsyncSession):
    """Test updating a mob with a name that already exists."""

    repo = repositories.MobRepository(session=database_session)
    slime_object = schemas.MobCreateSchema(name="Slime")
    skeleton_object = schemas.MobCreateSchema(name="Skeleton")
    slime = await repo.create(slime_object)
    await repo.create(skeleton_object)

    with pytest.raises(sql_exceptions.IntegrityError):
        await repo.update(slime.id, schemas.MobUpdateSchema(name="Skeleton"))


async def test_mob_update_not_existing(database_session: AsyncSession):
    """Test updating a mob that does not exist."""
    repo = repositories.MobRepository(session=database_session)

    with pytest.raises(domain_exceptions.DoesNotExistError):
        await repo.update(
            uuid.uuid4(), schemas.MobUpdateSchema(name="Skeleton")
        )
