"""Storage abstractions."""

from abc import ABC
from typing import Generic, Iterable, Type, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from monster_spawner.api.schemas import Schema as BaseSchema
from monster_spawner.database.exceptions import DoesNotExistError
from monster_spawner.database.generic.model import Base as BaseModel

Model = TypeVar("Model", bound=BaseModel)
InSchema = TypeVar("InSchema", bound=BaseSchema)
OutSchema = TypeVar("OutSchema", bound=BaseSchema)


class Repository(Generic[Model, InSchema, OutSchema], ABC):
    """Storage abstraction."""

    table: Type[Model]
    schema: Type[OutSchema]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data_object: InSchema) -> OutSchema:
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

    async def get_by_id(self, entry_id: UUID) -> OutSchema:
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
            raise DoesNotExistError(
                f"{self.table.__name__}<id:{entry_id}> does not exist",
            )
        return self.schema.from_orm(entry)

    async def collect(self) -> Iterable[OutSchema]:
        """Collect all entries.

        Returns:
            Iterable[OutSchema]: list of output data representations.
        """
        query = select(self.table)
        entries = await self.session.execute(query)
        return (self.schema.from_orm(entry) for entry in entries.scalars())
