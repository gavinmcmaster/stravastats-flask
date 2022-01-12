import json


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
