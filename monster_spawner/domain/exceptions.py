"""Custom exceptions for at the domain level."""

import uuid
from dataclasses import dataclass


@dataclass
class DoesNotExistError(Exception):
    """Raise when entry does not exist."""

    id: uuid.UUID
    entry_name: str = "Object"


@dataclass
class AlreadyExistsError(Exception):
    """Raise when entry already exists."""

    id: uuid.UUID
    entry_name: str = "Object"
