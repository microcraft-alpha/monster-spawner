"""Mob services."""

import uuid
from typing import Iterable

from structlog import get_logger

from monster_spawner.api.v1.mobs import schemas
from monster_spawner.domain import exceptions, repositories, transactions

logger = get_logger(__name__)


class MobService:
    """Mob model service."""

    def __init__(self, transaction: transactions.Transaction) -> None:
        self.transaction = transaction

    @property
    def repository(self) -> repositories.Repository:
        """Get the repository out of the transaction.

        Returns:
            Repository: storage class instance.
        """
        return self.transaction.repository

    async def create(
        self,
        data_object: schemas.MobInSchema,
    ) -> schemas.MobOutSchema:
        """Create a new mob.

        Args:
            data_object (MobInSchema): mob data.

        Raises:
            AlreadyExistsError: when mob already exists.

        Returns:
            MobOutSchema: mob output data.
        """
        logger.info("Creating mob", data=data_object)
        async with self.transaction:
            mobs = await self.repository.collect(name=data_object.name)
            if list(mobs):
                raise exceptions.AlreadyExistsError()
            mob = await self.repository.create(data_object)
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

    async def get_all(self) -> Iterable[schemas.MobOutSchema]:
        """Get all mobs.

        Returns:
            Iterable[MobOutSchema]: all mobs output data.
        """
        logger.info("Getting all mobs")
        mobs = await self.repository.collect()
        logger.info("Got all the mobs")
        return mobs
