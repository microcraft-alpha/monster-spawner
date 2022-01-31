"""Mob API schemas."""

from uuid import UUID

from monster_spawner.api import schemas


class MobCreateSchema(schemas.Schema):
    """Mob create input representation."""

    name: str
    hostile: bool = False


class MobUpdateSchema(schemas.Schema):
    """Mob update input representation."""

    name: str | None = None
    hostile: bool | None = None


class MobOutSchema(schemas.Schema):
    """Mob output representation."""

    id: UUID
    name: str
    hostile: bool
