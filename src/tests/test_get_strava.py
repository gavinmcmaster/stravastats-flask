import json
import os

def test_get_strava_app(client, login):
    # Set test environment variables
    os.environ['STRAVA_CLIENT_ID'] = 'test_client_id'
    os.environ['STRAVA_CLIENT_SECRET'] = 'test_client_secret'

    response = client.get(
        "/api/strava/app/key",
        headers=dict(
            Authorization='Bearer ' + login['auth_token']
        )
    )

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    
    data = json.loads(response.data.decode())
    assert data['strava_client_id'] == 'test_client_id'
    assert data['strava_client_secret'] == 'test_client_secret'