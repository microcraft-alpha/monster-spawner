"""Url filters."""

from dataclasses import dataclass

from fastapi import Query


@dataclass
class MobFilters:
    """Mob object filters."""

    name: str | None = Query(None)
    hostile: bool | None = Query(None)
