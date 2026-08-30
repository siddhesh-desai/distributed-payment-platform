"""Alembic environment — applies per-module migration version directories."""

from __future__ import annotations

import os
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

from core.alembic.import_module_models import import_module_models
from core.settings import get_settings
from payflow_common.models import OrmBaseModel

import_module_models()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = OrmBaseModel.metadata


def _module_version_locations() -> list[str]:
    """Discover `modules/<name>/migrations` directories (ADR-0004)."""
    api_root = Path(__file__).resolve().parents[2]
    modules_root = api_root / "modules"
    locations: list[str] = []
    if not modules_root.is_dir():
        return locations
    for module_dir in sorted(modules_root.iterdir()):
        if not module_dir.is_dir() or module_dir.name.startswith((".", "_")):
            continue
        migrations = module_dir / "migrations"
        if migrations.is_dir():
            locations.append(str(migrations))
    return locations


# Register module version paths for history/current/upgrade.
_version_locations = _module_version_locations()
if _version_locations:
    config.set_main_option(
        "version_locations",
        os.pathsep.join(_version_locations),
    )


def run_migrations_offline() -> None:
    url = get_settings().database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_locations=_version_locations,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_settings().database_url
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_locations=_version_locations,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
