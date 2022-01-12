"""Storage abstractions."""

import abc
from typing import Any, Generic, Iterable, TypeVar

from monster_spawner.api.v1.mobs import schemas

InSchema = TypeVar("InSchema", bound=schemas.Schema)
OutSchema = TypeVar("OutSchema", bound=schemas.Schema)


class Repository(Generic[InSchema, OutSchema], abc.ABC):
    """Storage abstraction."""

    def __init__(self, *args, **kwargs) -> None:
        """Allow taking parameters.

        Args:
            args: positional arguments.
            kwargs: keyword arguments.
        """

    @abc.abstractmethod
    async def create(self, data_object: InSchema) -> OutSchema:
        """Create a new entry.

        Args:
            data_object (InSchema): input data object.
        """

    @abc.abstractmethod
    async def get_by_id(self, entry_id: Any) -> OutSchema:
        """Get an entry by its identifier.

        Args:
            entry_id (Any): entry ID.
        """

    @abc.abstractmethod
    async def collect(self) -> Iterable[OutSchema]:
        """Collect all entries."""
