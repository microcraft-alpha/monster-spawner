"""Mob services."""

import uuid
from typing import Iterable

from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from structlog import get_logger

from monster_spawner.api.v1.mobs import schemas
from monster_spawner.database import models, sessions
from monster_spawner.domain import exceptions, repositories, transactions

log = get_logger()


class MobService:
    """Mob model service."""

    def __init__(
        self,
        repository: type[repositories.Repository],
        transaction: type[transactions.Transaction],
    ) -> None:
        self.repository_class = repository
        self.transaction_class = transaction

    def __call__(
        self,
        session: AsyncSession = Depends(sessions.get_session),  # type: ignore
    ) -> "MobService":
        """Initialize the dependencies with the database session.

        Args:
            session (AsyncSession): database session.

        Returns:
            MobService: service with the dependencies.
        """
        self.transaction = self.transaction_class(
            session,
            self.repository_class,
        )
        return self

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
        log.info("Creating mob", data=data_object)
        async with self.transaction:
            query = select(models.Mob).where(
                models.Mob.name == data_object.name,
            )
            mobs = await self.repository.collect(query)
            if list(mobs):
                raise exceptions.AlreadyExistsError()
            mob = await self.repository.create(data_object)
        log.info("Created mob", mob=mob)
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
        log.info("Getting mob", pk=pk)
        mob = await self.repository.get_by_id(pk)
        log.info("Got mob", mob=mob)
        return mob

    async def get_all(self) -> Iterable[schemas.MobOutSchema]:
        """Get all mobs.

        Returns:
            Iterable[MobOutSchema]: all mobs output data.
        """
        log.info("Getting all mobs")
        mobs = await self.repository.collect()
        log.info("Got all the mobs")
        return mobs
