import os
from dotenv import load_dotenv
import pytest
from stravastats import create_app
from stravastats.db import drop_db, reset_db


@pytest.fixture
def app():
    load_dotenv()

    test_config = {"TESTING": True}
    test_config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_UNIT_TEST_URI')
    test_config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv(
        'SQL_TRACK_MODS')

    app = create_app(test_config)
    app.testing = True

    with app.app_context():
        reset_db()

    yield app

    with app.app_context():
        drop_db()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
