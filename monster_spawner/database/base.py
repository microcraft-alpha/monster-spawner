"""Database model abstraction."""

import uuid
from typing import Any

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()


class Model(Base):  # type: ignore
    """Abstract database model."""

    __abstract__ = True
    __name__: str

    metadata: Any

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    @declared_attr
    def __tablename__(self) -> str:
        """Return the table name.

        Returns:
            str: lowercased name.
        """
        return self.__name__.lower()
