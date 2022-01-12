"""Database storage classes."""

import uuid
from typing import Generic, Iterable, Type, TypeVar

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from monster_spawner.database import base, exceptions
from monster_spawner.domain import repositories

Model = TypeVar("Model", bound=base.Model)


class ORMRepository(
    Generic[
        Model,
        repositories.InSchema,
        repositories.OutSchema,
    ],
    repositories.Repository[
        repositories.InSchema,
        repositories.OutSchema,
    ],
):
    """Generic database storage for ORM models."""

    table: Type[Model]
    schema: Type[repositories.OutSchema]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        data_object: repositories.InSchema,
    ) -> repositories.OutSchema:
        """Create a new entry.

        Args:
            data_object (InSchema): input data object.

        Returns:
            OutSchema: output data representation.
        """
        entry = self.table(**data_object.dict())
        self.session.add(entry)
        await self.session.commit()
        return self.schema.from_orm(entry)

    async def get_by_id(self, entry_id: uuid.UUID) -> repositories.OutSchema:
        """Get an entry by its id.

        Args:
            entry_id (UUID): primary key.

        Raises:
            DoesNotExistError: when entry does not exist.

        Returns:
            OutSchema: output data representation.
        """
        entry = await self.session.get(self.table, entry_id)
        if not entry:
            raise exceptions.DoesNotExistError(
                f"{self.table.__name__}<id:{entry_id}> does not exist",
            )
        return self.schema.from_orm(entry)

    async def collect(self) -> Iterable[repositories.OutSchema]:
        """Collect all entries.

        Returns:
            Iterable[OutSchema]: list of output data representations.
        """
        query = select(self.table)
        entries = await self.session.execute(query)
        return (self.schema.from_orm(entry) for entry in entries.scalars())