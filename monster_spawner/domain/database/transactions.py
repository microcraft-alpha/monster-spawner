"""Database transactions."""

from sqlalchemy.ext.asyncio.session import AsyncSession

from monster_spawner.domain import repositories, transactions


class DatabaseTransaction(transactions.Transaction):
    """Database unit of work."""

    def __init__(
        self,
        session: AsyncSession,
        repository: type[repositories.Repository],
    ) -> None:
        self.session = session
        self.repository = repository(session=session)

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
