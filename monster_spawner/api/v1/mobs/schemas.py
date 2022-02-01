"""Mob API schemas."""

from uuid import UUID

from monster_spawner.api import schemas


class MobCreateSchema(schemas.Schema):
    """Mob create input representation."""

    name: str
    hostile: bool = False
    health: int = 100
    damage: int = 10


class MobUpdateSchema(schemas.Schema):
    """Mob update input representation."""

    name: str | None = None
    hostile: bool | None = None
    health: int | None = None
    damage: int | None = None


class MobOutSchema(schemas.Schema):
    """Mob output representation."""

    id: UUID
    name: str
    hostile: bool
    health: int
    damage: int
