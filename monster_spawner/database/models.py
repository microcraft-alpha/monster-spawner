"""Database models."""

from sqlalchemy import Column, String

from monster_spawner.database.generic.model import Base


class Mob(Base):
    """Mob representation."""

    __name__ = "mobs"

    name = Column(String, unique=True)

    def __repr__(self) -> str:
        """Return a string representation of the model.

        Returns:
            str: string representation.
        """
        return f"<Mob {self.name} - {self.id}>"
