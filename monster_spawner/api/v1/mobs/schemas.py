"""API schemas."""

from uuid import UUID

from pydantic import BaseModel


class Schema(BaseModel):
    """Business model of a single entity."""

    class Config(BaseModel.Config):
        orm_mode = True


class MobInSchema(Schema):
    """Mob input representation."""

    name: str


class MobOutSchema(Schema):
    """Mob output representation."""

    id: UUID
    name: str
