import pytest
from db.database import get_db
from sqlalchemy.orm import Session


def test_get_db_yields_session():
    generator = get_db()
    db = next(generator)
    assert isinstance(db, Session)
    # closing generator should not raise
    try:
        next(generator)
    except StopIteration:
        pass

