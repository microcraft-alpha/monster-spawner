"""Storage abstractions."""

import typing as T  # noqa: WPS111,N812
import uuid

from monster_spawner.api import schemas

InSchema = T.TypeVar("InSchema", bound=schemas.Schema, contravariant=True)
OutSchema = T.TypeVar("OutSchema", bound=schemas.Schema, covariant=True)


class Repository(
    T.Generic[InSchema, OutSchema],
    T.Protocol,
):
    """Storage interface."""

    def __init__(self, *args, **kwargs) -> None:
        """Allow taking parameters."""  # noqa: DAR101

    async def create(self, data_object: InSchema) -> OutSchema:
        """Create a new entry.

        Args:
            data_object (InSchema): input data object.
        """
        ...  # noqa: WPS428

    async def get_by_id(self, entry_id: uuid.UUID) -> OutSchema:
        """Get an entry by its identifier.

        Args:
            entry_id (Any): entry ID.
        """
        ...  # noqa: WPS428

    async def collect(
        self,
        **filters,
    ) -> T.Iterable[OutSchema]:
        """Collect all entries and allow filtering.

        Args:
            filters (dict): additional filters to apply.
        """
        ...  # noqa: WPS428
