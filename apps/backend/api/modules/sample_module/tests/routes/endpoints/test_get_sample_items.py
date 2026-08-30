"""GET /sample/items route tests.

- Returns sample items from the facade for GET /sample/items
- Returns an empty list when the facade has no rows
- Surfaces a 500 when the facade raises unexpectedly
"""

from collections.abc import Generator
from unittest.mock import MagicMock, patch
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.db import get_db
from main import app
from modules.sample_module.models import SampleItem

_SEED_ID = UUID("11111111-1111-1111-1111-111111111111")
_FACADE_LIST = ".".join(
    (
        "modules.sample_module.routes.endpoints",
        "get_sample_items",
        "SampleItemFacade.list_items",
    )
)


def _override_db() -> Generator[Session, None, None]:
    yield MagicMock(spec=Session)


def test_get_sample_items() -> None:
    app.dependency_overrides[get_db] = _override_db
    try:
        with patch(
            _FACADE_LIST,
            return_value=[
                SampleItem(id=_SEED_ID, message="Hello from Postgres"),
            ],
        ):
            client = TestClient(app)
            response = client.get("/sample/items")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(_SEED_ID),
            "message": "Hello from Postgres",
        }
    ]


def test_get_sample_items_empty() -> None:
    app.dependency_overrides[get_db] = _override_db
    try:
        with patch(_FACADE_LIST, return_value=[]):
            client = TestClient(app)
            response = client.get("/sample/items")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == []


def test_get_sample_items_facade_error() -> None:
    app.dependency_overrides[get_db] = _override_db
    try:
        with patch(_FACADE_LIST, side_effect=RuntimeError("boom")):
            client = TestClient(app, raise_server_exceptions=False)
            response = client.get("/sample/items")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
