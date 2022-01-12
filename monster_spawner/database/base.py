"""Database model abstraction."""

import uuid
from typing import Any

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Model:
    """Abstract database model."""

    __name__: str

    metadata: Any

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    def __init__(self, *args, **kwargs) -> None:
        """Allow taking parameters.

        Args:
            args: positional arguments.
            kwargs: keyword arguments.
        """

    @declared_attr
    def __tablename__(self) -> str:
        """Return the table name.

        Returns:
            str: lowercased name.
        """
        return self.__name__.lower()
