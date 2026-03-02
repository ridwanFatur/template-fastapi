import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from services.user_service import get_or_create_user, get_user
from fastapi import HTTPException

# set up in-memory database for service tests
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_get_or_create_user_and_get_user():
    db = TestingSessionLocal()
    user, created = get_or_create_user(db, "test@example.com", "Test")
    assert created
    assert user.email == "test@example.com"
    fetched = get_user(db, user.id)
    assert fetched.id == user.id

    # calling again should return existing user
    user2, created2 = get_or_create_user(db, "test@example.com", "Test")
    assert not created2


def test_get_or_create_user_invalid_email():
    db = TestingSessionLocal()
    with pytest.raises(HTTPException):
        get_or_create_user(db, "not-an-email", "Name")
