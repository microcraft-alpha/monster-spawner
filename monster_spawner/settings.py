"""App settings."""

from environs import Env
from pydantic import BaseSettings

env = Env()


class Settings(BaseSettings):
    """Basic settings for the application."""

    TITLE: str = "Monster Spawner"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "Service handling Minecraft mobs"
    DEBUG: bool = env.bool("DEBUG", default=False)

    DATABASE_URL: str = env.str("DATABASE_URL")
    DATABASE_NAME: str = env.str("DATABASE_NAME")


settings = Settings()
