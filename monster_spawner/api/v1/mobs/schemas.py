"""Mob API schemas."""

from uuid import UUID

from monster_spawner.api import schemas


class MobInSchema(schemas.Schema):
    """Mob input representation."""

    name: str
    hostile: bool = False


class MobOutSchema(schemas.Schema):
    """Mob output representation."""

    id: UUID
    name: str
    hostile: bool = False
