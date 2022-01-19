"""Custom exceptions for at the domain level."""


class DoesNotExistError(Exception):
    """Raise when entry does not exist."""


class AlreadyExistsError(Exception):
    """Raise when entry already exists."""
