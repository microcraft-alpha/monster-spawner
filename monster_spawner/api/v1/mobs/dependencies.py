"""Dependencies for the Mob API."""

from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from structlog import get_logger

from monster_spawner.database import sessions
from monster_spawner.domain.database import transactions
from monster_spawner.domain.mob import repositories, services

logger = get_logger(__name__)


def get_alchemy_mob_service(
    session: AsyncSession = Depends(sessions.get_session),  # type: ignore
) -> services.MobService:
    """Instantiate a MobService with a database session.

    Args:
        session (AsyncSession): database session.

    Returns:
        MobService: mob service.
    """
    transaction = transactions.DatabaseTransaction(
        session,
        repositories.MobRepository,
    )
    return services.MobService(transaction=transaction)
