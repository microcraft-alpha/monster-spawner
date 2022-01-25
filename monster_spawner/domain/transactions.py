"""Transaction abstractions."""

import abc

from monster_spawner.domain import repositories


class Transaction(abc.ABC):
    """Unit of work abstraction."""

    repository: repositories.Repository

    def __init__(self, *args, **kwargs) -> None:
        """Allow taking parameters."""  # noqa: DAR101

    async def __aenter__(self) -> "Transaction":
        """Start the transaction.

        Returns:
            Transaction: started transaction.
        """
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """Exit and rollback the transaction."""  # noqa: DAR101
        await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None:
        """Commit the transaction."""

    @abc.abstractmethod
    async def rollback(self) -> None:
        """Rollback the transaction."""
