"""App settings."""

from environs import Env
from pydantic import BaseSettings

env = Env()


class Settings(BaseSettings):
    """Basic settings for the application."""

    TITLE: str = "Monster Spawner"
    VERSION: str = "0.0.1"
    DESCRIPTION: str = "Service handling Minecraft monsters"
    DEBUG: bool = env.bool("DEBUG", False)

    DATABASE_URL: str = env.str("DATABASE_URL")


settings = Settings()
