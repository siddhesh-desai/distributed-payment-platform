"""PostgreSQL / SQLAlchemy connection settings."""

from pydantic import Field, computed_field

from core.settings.base import SettingsBase


class DatabaseSettings(SettingsBase):
    """Discrete DB knobs; builds the SQLAlchemy URL."""

    postgres_user: str = Field(default="payflow")
    postgres_password: str = Field(default="payflow")
    postgres_db: str = Field(default="payflow")
    postgres_host: str = Field(default="localhost", description="Host")
    postgres_port: int = Field(default=5433, description="Postgres port")
    postgres_pool_size: int = Field(default=5, ge=1, le=100)
    postgres_pool_timeout_seconds: int = Field(default=30, ge=1, le=300)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        """SQLAlchemy URL built from discrete DB settings."""
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
