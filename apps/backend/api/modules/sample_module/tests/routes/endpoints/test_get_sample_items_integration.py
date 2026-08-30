"""Live Postgres smoke for GET /sample/items.

- Returns seeded sample rows when Compose Postgres is reachable and migrated
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from core.settings import get_settings
from main import app

_SEED_ID = "11111111-1111-1111-1111-111111111111"
_SEED_MESSAGE = "Hello from Postgres"
_SKIP_REASON = "Postgres not reachable (start Compose)"


def _postgres_ready() -> bool:
    try:
        engine = create_engine(get_settings().database_url, pool_pre_ping=True)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def _is_seed_row(row: dict[str, object]) -> bool:
    return row.get("id") == _SEED_ID and row.get("message") == _SEED_MESSAGE


@pytest.mark.skipif(not _postgres_ready(), reason=_SKIP_REASON)
def test_get_sample_items_against_postgres() -> None:
    client = TestClient(app)
    response = client.get("/sample/items")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(_is_seed_row(row) for row in body)
