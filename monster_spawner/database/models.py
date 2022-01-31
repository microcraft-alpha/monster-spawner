"""Database models."""

from sqlalchemy import Boolean, Column, String

from monster_spawner.database import base


class Mob(base.Model):
    """Mob representation."""

    __name__ = "mobs"

    name = Column(String, nullable=False, unique=True)
    hostile = Column(Boolean, nullable=False, default=False)
