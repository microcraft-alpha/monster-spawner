"""Storage classes."""

from monster_spawner.api.schemas import MobInSchema, MobOutSchema
from monster_spawner.database.generic.repository import Repository
from monster_spawner.database.models import Mob


class MobRepository(Repository[Mob, MobInSchema, MobOutSchema]):
    """Mob storage."""

    table = Mob
    schema = MobOutSchema
