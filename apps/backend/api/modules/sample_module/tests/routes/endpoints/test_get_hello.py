"""GET /sample/hello route tests.

- Returns the sample hello payload for GET /sample/hello
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_sample_hello() -> None:
    response = client.get("/sample/hello")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, world",
        "module": "sample_module",
    }
