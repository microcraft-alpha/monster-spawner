"""Database storage classes."""

import typing as T  # noqa: WPS111,N812
import uuid

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from monster_spawner.database import base
from monster_spawner.domain import exceptions, repositories
from monster_spawner.domain.database import queries

Model = T.TypeVar("Model", bound=base.Model)


class AlchemyRepository(
    T.Generic[
        Model,
        repositories.CreateSchema,
        repositories.UpdateSchema,
        repositories.OutSchema,
    ],
):
    """Generic database storage for ORM models."""

    table: type[Model]
    schema: type[repositories.OutSchema]

    def __init__(self, *args, session: AsyncSession, **kwargs) -> None:
        self.session = session

    async def create(
        self,
        data_object: repositories.CreateSchema,
    ) -> repositories.OutSchema:
        """Create a new entry.

        Args:
            data_object (CreateSchema): input data object.

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
                id=entry_id,
                entry_name=self.table.__name__,
            )
        return self.schema.from_orm(entry)

    async def collect(
        self,
        **filters,
    ) -> T.Iterable[repositories.OutSchema]:
        """Collect all entries nased on the query.

        Args:
            filters (dict): filters to apply.

        Returns:
            Iterable[OutSchema]: list of output data representations.
        """
        if filters:
            filter_expressions = queries.create_expressions(self.table, filters)
            query = select(self.table).where(*filter_expressions)
        else:
            query = select(self.table)
        entries = await self.session.execute(query)
        return (self.schema.from_orm(entry) for entry in entries.scalars())

    async def delete(self, entry_id: uuid.UUID) -> None:
        """Get an entry by its id and delete it.

        Args:
            entry_id (UUID): primary key.
        """
        await self.get_by_id(entry_id)
        query = delete(self.table).where(self.table.id == entry_id)
        await self.session.execute(query)

    async def update(
        self,
        entry_id: uuid.UUID,
        data_object: repositories.UpdateSchema,
    ) -> repositories.OutSchema:
        """Update an existing entry.

        Args:
            entry_id (UUID): primary key.
            data_object (CreateSchema): input data object.

        Returns:
            OutSchema: output data representation.
        """
        query = (
            update(self.table)
            .where(self.table.id == entry_id)
            .values(**data_object.dict(exclude_unset=True))
        )
        await self.session.execute(query)

        entry = await self.get_by_id(entry_id)
        return self.schema.from_orm(entry)
