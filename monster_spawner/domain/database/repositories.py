"""Database storage classes."""

import typing as T  # noqa: WPS111,N812
import uuid

from sqlalchemy import sql
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from monster_spawner.database import base
from monster_spawner.domain import exceptions, repositories

Model = T.TypeVar("Model", bound=base.Model)


class AlchemyRepository(
    T.Generic[
        Model,
        repositories.InSchema,
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
            raise exceptions.DoesNotExistError()
        return self.schema.from_orm(entry)

    async def collect(
        self,
        query: T.Optional[sql.Select] = None,
    ) -> T.Iterable[repositories.OutSchema]:
        """Collect all entries nased on the query.

        Args:
            query (Optional[Select]): sql query object.
                Defaults to 'select(self.table)'.

        Returns:
            Iterable[OutSchema]: list of output data representations.
        """
        if query is None:
            query = select(self.table)
        entries = await self.session.execute(query)
        return (self.schema.from_orm(entry) for entry in entries.scalars())
