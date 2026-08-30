"""Process-level health smoke (hosted here until an ops surface exists).

- Returns ok for GET /health
"""

from fastapi.testclient import TestClient

from main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
