import json
from stravastats.db import get_db
from stravastats.api.models import Gear


def test_add_gear(app, client, login):
    body = {"strava_gear_id": "zy56538745",
            "primary": 0,
            "name": "Boardman Team 2013",
            "retired": 0,
            "brand_name": "Boardman",
            "model_name": "Team 2013",
            "description": "",
            "weight": 9.0,
            "created_at": 1619765803
            }

    response = client.post(
        "/gear/add", json=body, headers=dict(
            Authorization='Bearer ' + login['auth_token']
        )
    )
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    data = json.loads(response.data.decode())
    assert data['message'] == "Gear 'Boardman Team 2013' added"

    with app.app_context():
        db = get_db()
        count = db.session.query(Gear.id).count()
        assert count == 1


def test_get_gears(client, login):
    response = client.get("/gears", headers=dict(
        Authorization='Bearer ' + login['auth_token']
    ))
    assert response.status_code == 200
