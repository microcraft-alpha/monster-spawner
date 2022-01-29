"""Database models."""

from sqlalchemy import Boolean, Column, String

from monster_spawner.database import base


class Mob(base.Model):
    """Mob representation."""

    __name__ = "mobs"

    name = Column(String, unique=True)
    hostile = Column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        """Return a string representation of the model.

        Returns:
            str: string representation.
        """
        return f"<Mob {self.name} - {self.id}>"
