"""Mob services."""

import typing as T  # noqa: WPS111,N812
import uuid

from structlog import get_logger

from monster_spawner.api.v1.mobs import schemas
from monster_spawner.domain import exceptions, repositories, transactions
from monster_spawner.domain.events.outgoing import (
    MonsterCreated,
    MonsterDeleted,
)
from monster_spawner.events.bus import EventBus

logger = get_logger(__name__)


class MobService:
    """Mob model service."""

    def __init__(
        self,
        transaction: transactions.Transaction,
        repository: repositories.Repository,
    ) -> None:
        self.transaction = transaction
        self.repository = repository

    async def create(
        self,
        data_object: schemas.MobCreateSchema,
    ) -> schemas.MobOutSchema:
        """Create a new mob.

        Args:
            data_object (MobCreateSchema): mob data.

        Raises:
            AlreadyExistsError: when mob already exists.

        Returns:
            MobOutSchema: mob output data.
        """
        logger.info("Creating mob", data=data_object)
        async with self.transaction:
            mobs = await self.repository.collect(name=data_object.name)
            mobs = list(mobs)
            if mobs:
                raise exceptions.AlreadyExistsError(
                    id=mobs[0].id,
                    entry_name="Mob",
                )
            mob = await self.repository.create(data_object)
            await self.transaction.commit()
            await EventBus.publish(MonsterCreated(**mob.dict()))
        logger.info("Created mob", mob=mob)
        return mob

    async def get(
        self,
        pk: uuid.UUID,
    ) -> schemas.MobOutSchema:
        """Get a mob by its primary key.

        Args:
            pk (UUID): mob primary key.

        Returns:
            MobOutSchema: mob output data.
        """
        logger.info("Getting mob", pk=pk)
        mob = await self.repository.get_by_id(pk)
        logger.info("Got mob", mob=mob)
        return mob

    async def get_all(
        self,
        **filters,
    ) -> T.Iterable[schemas.MobOutSchema]:
        """Get all mobs.

        Args:
            filters (dict): filters to apply.

        Returns:
            Iterable[MobOutSchema]: all mobs output data.
        """
        logger.info("Getting all mobs")
        mobs = await self.repository.collect(**filters)
        logger.info("Got all the mobs")
        return mobs

    async def delete(self, pk: uuid.UUID) -> None:
        """Delete a mob by its primary key.

        Args:
            pk (UUID): mob primary key.
        """
        logger.info("Deleting mob", pk=pk)
        async with self.transaction:
            await self.repository.delete(pk)
            await self.transaction.commit()
            await EventBus.publish(MonsterDeleted(id=pk))
        logger.info("Deleted mob", pk=pk)

    async def update(
        self,
        pk: uuid.UUID,
        data_object: schemas.MobUpdateSchema,
    ) -> schemas.MobOutSchema:
        """Update an existing mob.

        Args:
            pk (UUID): mob primary key.
            data_object (MobCreateSchema): mob data.

        Raises:
            AlreadyExistsError: when mob already exists.

        Returns:
            MobOutSchema: mob output data.
        """
        logger.info("Updating mob", pk=pk, data=data_object)
        async with self.transaction:
            mobs = await self.repository.collect(name=data_object.name)
            mobs = list(mobs)
            if mobs and str(mobs[0].id) != str(pk):
                raise exceptions.AlreadyExistsError(
                    id=mobs[0].id,
                    entry_name="Mob",
                )
            mob = await self.repository.update(pk, data_object)
            await self.transaction.commit()
        logger.info("Updated mob", pk=pk)
        return mob
