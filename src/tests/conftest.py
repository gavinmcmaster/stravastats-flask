import os
import pytest
from stravastats import create_app
from stravastats.db import drop_db, reset_db, get_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    app.testing = True

    with app.app_context():
        reset_db()
        # get_db().engine.execute(_data_sql)

    yield app

    # drop_db()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
