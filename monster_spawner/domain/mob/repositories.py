"""Storage classes."""

from monster_spawner.api.v1.mobs import schemas
from monster_spawner.database import models
from monster_spawner.domain.database import repositories


class MobRepository(
    repositories.AlchemyRepository[
        models.Mob,
        schemas.MobCreateSchema,
        schemas.MobUpdateSchema,
        schemas.MobOutSchema,
    ],
):
    """Mob database storage."""

    table = models.Mob
    schema = schemas.MobOutSchema
