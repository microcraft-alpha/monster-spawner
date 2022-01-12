"""Transaction abstractions."""

import abc


class Transaction(abc.ABC):
    """Unit of work abstraction."""

    def __init__(self, *args, **kwargs) -> None:
        """Allow taking parameters.

        Args:
            args: positional arguments.
            kwargs: keyword arguments.
        """

    async def __aenter__(self) -> "Transaction":
        """Start the transaction.

        Returns:
            Transaction: started transaction.
        """
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """Exit and rollback the transaction.

        Args:
            args: positional arguments.
            kwargs: keyword arguments.
        """
        await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None:
        """Commit the transaction."""

    @abc.abstractmethod
    async def rollback(self) -> None:
        """Rollback the transaction."""
