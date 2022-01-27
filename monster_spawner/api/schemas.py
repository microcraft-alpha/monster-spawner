"""API schemas."""

from pydantic import BaseModel


class Schema(BaseModel):
    """Business model of a single entity."""

    class Config(BaseModel.Config):
        orm_mode = True
