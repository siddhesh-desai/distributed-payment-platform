"""SQLAlchemy engine (connection pool to Postgres)."""

from sqlalchemy import Engine, create_engine

from core.settings import get_settings


def build_engine() -> Engine:
    """Create an engine from settings (pool size, timeouts, pre-ping)."""
    settings = get_settings()
    return create_engine(
        settings.database_url,
        pool_size=settings.postgres_pool_size,
        pool_timeout=settings.postgres_pool_timeout_seconds,
        pool_pre_ping=True,
    )


engine = build_engine()
