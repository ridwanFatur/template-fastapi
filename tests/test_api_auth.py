from fastapi.testclient import TestClient
from main import app
from fastapi import HTTPException

client = TestClient(app)


def test_get_google_config():
    resp = client.get("/api/auth/google/config")
    assert resp.status_code == 200
    data = resp.json()
    assert "client_id" in data


def test_login_invalid_code(monkeypatch):
    def fake_google(auth_code):
        raise HTTPException(status_code=400, detail="Invalid Auth Code")

    monkeypatch.setattr(
        "services.google_service.get_google_user_details", fake_google)

    resp = client.post(
        "/api/auth/login", json={"auth_code": "bad"})
    assert resp.status_code == 400
