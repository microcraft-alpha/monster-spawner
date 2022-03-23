"""Event bus."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from structlog import get_logger

from monster_spawner.events.publisher import publish_with_redis

if TYPE_CHECKING:
    from monster_spawner.domain.events.event_types import Event
    from monster_spawner.events.event_types import EventType

logger = get_logger(__name__)


class EventBus:
    """Dispatcher and publisher for event objects."""

    events: dict[str, type["Event"]] = {}

    @classmethod
    async def publish(cls, event: "Event") -> None:
        """Publish an event to redis.

        Args:
            event (Event): event object.
        """
        logger.info(
            "Publishing event",
            event_object=event,
        )
        if not cls.events.get(event.event_type.value):
            logger.warning(
                "No event registered to publish",
                event_object=event,
                events=cls.events,
            )
            return
        await event.handle()
        publish_with_redis(event)


def eventclass(event_type: "EventType") -> Callable:
    """Register an event class and return it as a dataclass.

    Connector between the event type and the event class (dataclass).

    Args:
        event_type (EventType): event type - channel name.

    Returns:
        Callable: a decorator.
    """
    logger.info("Registering event class", event_type=event_type)

    def wrapper(cls) -> type:
        """Register the event class and create the dataclass.

        Args:
            cls (type): event class.

        Returns:
            type: the dataclass.
        """
        EventBus.events[event_type.value] = cls
        cls.event_type = event_type
        return dataclass(cls)

    return wrapper
