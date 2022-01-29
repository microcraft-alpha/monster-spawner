"""Mob API E2E test cases."""

import uuid

import pytest
from fastapi import status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_mob_create(async_client: AsyncClient):
    """Test creating a mob."""
    response = await async_client.post(
        "/api/v1/mobs/", json={"name": "Creeper"}
    )
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] is not None
    assert data["name"] == "Creeper"


async def test_mob_create_not_unique(async_client: AsyncClient):
    """Test creating a mob with a name that already exists."""
    await async_client.post("/api/v1/mobs/", json={"name": "Zombie"})

    response = await async_client.post("/api/v1/mobs/", json={"name": "Zombie"})
    data = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert data["detail"] == "Mob already exists"


async def test_mob_list(async_client: AsyncClient):
    """Test retrieving a list of mobs."""
    # Add 3 mobs to the database
    for i in range(3):
        await async_client.post("/api/v1/mobs/", json={"name": f"Zombie {i}"})

    response = await async_client.get("/api/v1/mobs/")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 3


async def test_mob_list_with_filters(async_client: AsyncClient):
    """Test retrieving a list of mobs with filters applied."""
    # Add 3 mobs to the database
    for i in range(3):
        await async_client.post("/api/v1/mobs/", json={"name": f"Zombie {i}"})

    response = await async_client.get("/api/v1/mobs/?name=Zombie 1")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1


async def test_mob_get(async_client: AsyncClient):
    """Test retrieving a single mob."""
    response = await async_client.post("/api/v1/mobs/", json={"name": "Zombie"})
    mob = response.json()

    response = await async_client.get(f"/api/v1/mobs/{mob['id']}")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == str(mob["id"])


async def test_mob_get_not_existing(async_client: AsyncClient):
    """Test retrieving a not existing mob."""
    response = await async_client.get(f"/api/v1/mobs/{uuid.uuid4()}")
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == "Mob does not exist"
