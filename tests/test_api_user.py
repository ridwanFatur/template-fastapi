from fastapi import Request
from fastapi.testclient import TestClient
from main import app
import jwt
from utils.config import SECRET_KEY, ALGORITHM
from dependencies.auth_middleware import get_current_user

client = TestClient(app)


def fake_get_current_user(request: Request, db=None):
    request.state.user = {"id": 123, "name": "Dummy"}


def test_fetch_user():
    app.dependency_overrides[get_current_user] = fake_get_current_user

    token = jwt.encode({"user_id": 123}, SECRET_KEY, algorithm=ALGORITHM)
    headers = {
        "Authorization": f"Bearer {token}"
    }

    resp = client.get("/api/user/", headers=headers)
    assert resp.status_code == 200

    app.dependency_overrides.clear()
