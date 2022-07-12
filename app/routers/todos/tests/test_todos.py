from fastapi.testclient import TestClient

from app.config import settings
from app.main import app

client = TestClient(app)
BAD_TOKEN = "BAD_TOKEN"
BASE_PATH = "/v1/todos"


def test_get_todos():
    """
    Test fetching todos
    """
    # No access token provided
    r = client.get(BASE_PATH)
    assert r.status_code == 403

    # Invalid access token
    r = client.get(
        BASE_PATH,
        headers={"Authorization": f"Bearer {BAD_TOKEN}"},
    )
    assert r.status_code == 401

    # Valid static token
    r = client.get(
        BASE_PATH,
        headers={"Authorization": f"Bearer {settings.static_token}"},
    )
    assert r.status_code == 200


def test_get_todos_bad_param():
    """
    Test fetching todos with invalid params
    """
    # Invalid limit
    r = client.get(
        f"{BASE_PATH}?limit=10000",
        headers={"Authorization": f"Bearer {settings.static_token}"},
    )
    assert r.status_code == 422
