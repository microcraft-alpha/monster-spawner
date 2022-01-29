"""Database transactions."""

from sqlalchemy.ext.asyncio.session import AsyncSession

from monster_spawner.domain import transactions


class DatabaseTransaction(transactions.Transaction):
    """Database unit of work."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __aexit__(self, *args, **kwargs) -> None:
        """Exit transaction and close the session."""  # noqa: DAR101
        await super().__aexit__(*args, **kwargs)
        await self.session.close()

    async def commit(self) -> None:
        """Commit the transaction."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the transaction."""
        await self.session.rollback()
