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
    mob = await async_client.post("/api/v1/mobs/", json={"name": "Zombie"})

    response = await async_client.post("/api/v1/mobs/", json={"name": "Zombie"})
    data = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert data["detail"] == f"Mob already exists - {mob.json()['id']}"


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
    mob_pk = uuid.uuid4()
    response = await async_client.get(f"/api/v1/mobs/{mob_pk}")
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == f"Mob does not exist - {mob_pk}"


async def test_mob_delete(async_client: AsyncClient):
    """Test deleting a mob."""
    # Add a mob
    response = await async_client.post("/api/v1/mobs/", json={"name": "Zombie"})
    mob = response.json()

    # Delete the mob
    response = await async_client.delete(f"/api/v1/mobs/{mob['id']}")
    data = response.json()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert data is None

    # Check that the mob is gone
    response = await async_client.get(f"/api/v1/mobs/{mob['id']}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_mob_delete_not_existing(async_client: AsyncClient):
    """Test deleting a not existing mob."""
    mob_pk = uuid.uuid4()
    response = await async_client.delete(f"/api/v1/mobs/{mob_pk}")
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == f"Mob does not exist - {mob_pk}"


async def test_mob_update(async_client: AsyncClient):
    """Test updating a mob."""
    response = await async_client.post("/api/v1/mobs/", json={"name": "Zombie"})
    mob = response.json()

    response = await async_client.patch(
        f"/api/v1/mobs/{mob['id']}", json={"name": "Creeper"}
    )
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == str(mob["id"])
    assert data["name"] == "Creeper"


async def test_mob_update_not_unique_name(async_client: AsyncClient):
    """Test updating a mob with a name that already exists."""
    # Add a mob
    response = await async_client.post("/api/v1/mobs/", json={"name": "Zombie"})
    zombie = response.json()

    # Add a mob with a different name
    response = await async_client.post(
        "/api/v1/mobs/", json={"name": "Creeper"}
    )
    creeper = response.json()

    # Update the mob with the same name
    response = await async_client.patch(
        f"/api/v1/mobs/{creeper['id']}", json={"name": "Zombie"}
    )
    data = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert data["detail"] == f"Mob already exists - {zombie['id']}"


async def test_mob_update_not_existing(async_client: AsyncClient):
    """Test updating a not existing mob."""
    mob_pk = uuid.uuid4()
    response = await async_client.patch(
        f"/api/v1/mobs/{mob_pk}", json={"name": "Zombie"}
    )
    data = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == f"Mob does not exist - {mob_pk}"
