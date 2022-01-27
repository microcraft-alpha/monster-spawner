"""V1 api router."""

from fastapi.routing import APIRouter

from monster_spawner.api.v1.mobs import routes

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(routes.router)
