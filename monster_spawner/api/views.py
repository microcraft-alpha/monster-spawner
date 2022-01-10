"""Mobs API routes."""

# TODO: Remove '# type: ignore' when sqlalchemy fixes generator issue.

from typing import Iterable
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from monster_spawner.api.schemas import MobInSchema, MobOutSchema
from monster_spawner.database.repositories import MobRepository
from monster_spawner.database.session import get_session

router = APIRouter(prefix="/mobs", tags=["mobs"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MobOutSchema,
)
async def create_mob(
    payload: MobInSchema,
    session: AsyncSession = Depends(get_session),  # type: ignore
) -> MobOutSchema:
    """Create a new mob.

    Args:
        payload (MobInSchema): mob input data.
        session (AsyncSession): database session.

    Returns:
        MobOutSchema: mob output data.
    """
    mob_repository = MobRepository(session)
    return await mob_repository.create(payload)


@router.get(
    "/{pk}",
    status_code=status.HTTP_200_OK,
    response_model=MobOutSchema,
)
async def get_mob(
    pk: UUID,
    session: AsyncSession = Depends(get_session),  # type: ignore
) -> MobOutSchema:
    """Get a mob by its primary key.

    Args:
        pk (UUID): primary key of the mob.
        session (AsyncSession): database session.

    Returns:
        MobOutSchema: mob output data.
    """
    mob_repository = MobRepository(session)
    return await mob_repository.get_by_id(pk)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Iterable[MobOutSchema],
)
async def get_mobs(
    session: AsyncSession = Depends(get_session),  # type: ignore
) -> Iterable[MobOutSchema]:
    """Get all mobs.

    Args:
        session (AsyncSession): database session.

    Returns:
        Iterable[MobOutSchema]: list of mobs output data.
    """
    mob_repository = MobRepository(session)
    return await mob_repository.collect()
