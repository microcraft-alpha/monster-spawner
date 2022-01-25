"""Mobs API routes."""

from typing import Iterable
from uuid import UUID

from fastapi import APIRouter
from fastapi import exceptions as http_exceptions
from fastapi.params import Depends
from starlette import status

from monster_spawner.api.v1.mobs import schemas
from monster_spawner.domain import exceptions
from monster_spawner.domain.database import transactions
from monster_spawner.domain.mob import repositories, services

router = APIRouter(prefix="/mobs", tags=["mobs"])

mob_service = services.MobService(
    repositories.MobRepository,
    transactions.DatabaseTransaction,
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MobOutSchema,
)
async def create_mob(
    payload: schemas.MobInSchema,
    service: services.MobService = Depends(mob_service),  # type: ignore
) -> schemas.MobOutSchema:
    """Create a new mob.

    Args:
        payload (MobInSchema): mob input data.
        service (MobService): mob service.

    Raises:
        HTTPException: when mob already exists.

    Returns:
        MobOutSchema: mob output data.
    """
    try:
        return await service.create(payload)
    except exceptions.AlreadyExistsError:
        raise http_exceptions.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mob already exists",
        )


@router.get(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MobOutSchema,
)
async def get_mob(
    pk: UUID,
    service: services.MobService = Depends(mob_service),  # type: ignore
) -> schemas.MobOutSchema:
    """Get mob by its primary key.

    Args:
        pk (UUID): primary key of the mob.
        service (MobService): mob service.

    Raises:
        HTTPException: when mob does not exist.

    Returns:
        MobOutSchema: mob output data.
    """
    try:
        return await service.get(pk)
    except exceptions.DoesNotExistError:
        raise http_exceptions.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mob does not exist",
        )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Iterable[schemas.MobOutSchema],
)
async def get_mobs(
    service: services.MobService = Depends(mob_service),  # type: ignore
) -> Iterable[schemas.MobOutSchema]:
    """Get all mobs.

    Args:
        service (MobService): mob service.

    Returns:
        Iterable[MobOutSchema]: list of mobs output data.
    """
    return await service.get_all()
