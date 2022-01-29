"""Dependencies for the Mob API."""

import typing as T  # noqa: WPS111,N812

from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from structlog import get_logger

from monster_spawner.database import sessions
from monster_spawner.domain.database import transactions
from monster_spawner.domain.mob import repositories, services

logger = get_logger(__name__)

DictItems = list[tuple[str, T.Any]]


def get_alchemy_mob_service(
    session: AsyncSession = Depends(sessions.get_session),  # type: ignore
) -> services.MobService:
    """Instantiate a MobService with a database session.

    Args:
        session (AsyncSession): database session.

    Returns:
        MobService: mob service.
    """
    transaction = transactions.DatabaseTransaction(session=session)
    repository = repositories.MobRepository(session=session)
    return services.MobService(transaction, repository)


def dict_factory(dict_items: DictItems) -> dict[str, T.Any]:
    """Convert a list of tuples to a dictionary.

    Args:
        dict_items (DictItems): list of tuples.

    Returns:
        dict[str, Any]: dictionary without empty values.
    """
    return {key: value for key, value in dict_items if value}  # noqa: WPS110
