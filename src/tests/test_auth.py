import json
from stravastats.api.models import User
from stravastats.db import get_db


def test_registration(client):
    response = client.post('/auth/register',
                           data=json.dumps(dict(
                               email='gavin@invalid.com',
                               password='123456'
                           )),
                           content_type='application/json'
                           )
    data = json.loads(response.data.decode())
    assert data['message'] == 'User successfully registered'
    assert data['auth_token']
    assert response.content_type == 'application/json'
    assert response.status_code == 201


def test_registered_user_login(app, client):
    with app.app_context():
        db = get_db()
        user = User(
            email='gavin@invalid.com',
            password='123456'
        )
        db.session.add(user)
        db.session.commit()

        response = client.post('/auth/login',
                               data=json.dumps(dict(
                                   email='gavin@invalid.com',
                                   password='123456'
                               )),
                               content_type='application/json'
                               )
        data = json.loads(response.data.decode())
        assert data['message'] == 'User successfully logged in'
        assert data['auth_token']
        assert data['status'] == 'success'
        assert response.content_type == 'application/json'
        assert response.status_code == 200


def test_unregistered_user_login_attempt(app, client):
    response = client.post('/auth/login',
                           data=json.dumps(dict(
                               email='unregistered@invalid.com',
                               password='123456'
                           )),
                           content_type='application/json'
                           )
    data = json.loads(response.data.decode())
    assert data['message'] == 'Invalid user credentials'
    assert data['status'] == 'fail'
    assert response.content_type == 'application/json'
    assert response.status_code == 401
