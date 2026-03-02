import pytest
from dependencies.auth_middleware import parse_jwt_for_user_id
from fastapi import HTTPException
import jwt
from utils.config import SECRET_KEY, ALGORITHM


class DummyRequest:
    def __init__(self, headers):
        self.headers = headers


def test_parse_jwt_success():
    token = jwt.encode({"user_id": 42}, SECRET_KEY, algorithm=ALGORITHM)
    req = DummyRequest({"Authorization": f"Bearer {token}"})
    assert parse_jwt_for_user_id(req) == 42


def test_parse_jwt_missing_header():
    req = DummyRequest({})
    with pytest.raises(HTTPException):
        parse_jwt_for_user_id(req)


def test_parse_jwt_invalid_token():
    req = DummyRequest({"Authorization": "Bearer badtoken"})
    with pytest.raises(HTTPException):
        parse_jwt_for_user_id(req)


def test_parse_jwt_no_user_id():
    token = jwt.encode({"foo": "bar"}, SECRET_KEY, algorithm=ALGORITHM)
    req = DummyRequest({"Authorization": f"Bearer {token}"})
    with pytest.raises(HTTPException):
        parse_jwt_for_user_id(req)
