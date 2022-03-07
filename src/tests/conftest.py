import pytest
import os
import json
from dotenv import load_dotenv
from stravastats import create_app
from stravastats.db import drop_db, reset_db, get_db
from stravastats.api.models import User


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


@pytest.fixture
def login(app, client):
    with app.app_context():
        db = get_db()
        user = User(
            email='gavin@invalid.com',
            password='123456'
        )
        db.session.add(user)
        db.session.commit()

        login_response = client.post('/auth/login',
                                     data=json.dumps(dict(
                                         email='gavin@invalid.com',
                                         password='123456'
                                     )),
                                     content_type='application/json'
                                     )
        login_data = json.loads(login_response.data.decode())
        return login_data
