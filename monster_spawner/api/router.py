"""Api router."""

from fastapi import APIRouter

from monster_spawner.api.v1 import router

api_router = APIRouter(prefix="/api")
api_router.include_router(router.v1_router)
