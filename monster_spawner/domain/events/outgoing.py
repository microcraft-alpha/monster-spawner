"""Domain events going to the outside world."""


import uuid

from structlog import get_logger

from monster_spawner.domain.events.event_types import Event
from monster_spawner.events.bus import eventclass
from monster_spawner.events.event_types import OutgoingEventType

logger = get_logger(__name__)


@eventclass(OutgoingEventType.MONSTER_CREATED)
class MonsterCreated(Event):
    """Event handler for monster creation."""

    id: uuid.UUID
    name: str
    hostile: bool
    health: int
    damage: int

    async def handle(self) -> None:
        """Publish info about created monster."""


@eventclass(OutgoingEventType.MONSTER_DELETED)
class MonsterDeleted(Event):
    """Event handler for monster deletion."""

    id: uuid.UUID

    async def handle(self) -> None:
        """Publish info about deleted monster."""
