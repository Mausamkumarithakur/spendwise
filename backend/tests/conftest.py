"""Shared test fixtures."""
import pytest
from app import create_app
from models import db as _db
from config import TestConfig


@pytest.fixture(scope="session")
def app():
    app = create_app(TestConfig)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Wipe tables between tests to keep them isolated."""
    yield
    with app.app_context():
        _db.session.execute(_db.text("DELETE FROM expenses"))
        _db.session.commit()
