"""Database queries helpers."""

import typing as T  # noqa: WPS111,N812

from sqlalchemy.sql import elements

from monster_spawner.database import base


def create_expressions(
    model: type[base.Model],
    filters: dict[str, T.Any],
) -> list[elements.BinaryExpression]:
    """Create SQL binary expressions from filters.

    Args:
        model (type[Model]): alchemy model.
        filters (dict[str, Any]): filters.

    Returns:
        list[BinaryExpression]: created expressions.
    """
    return [
        getattr(model, field) == value
        for field, value in filters.items()  # noqa: WPS110
    ]
