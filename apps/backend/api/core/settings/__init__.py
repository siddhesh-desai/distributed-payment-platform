"""Composed application settings (import from `core.settings`)."""

from functools import lru_cache

from core.settings.database import DatabaseSettings


class Settings(DatabaseSettings):
    """
    Merged runtime settings.
    Add more mixins as groups grow (e.g. `RedisSettings`).
    """


@lru_cache
def get_settings() -> Settings:
    return Settings()
