import json
from sqlalchemy import insert
from stravastats.db import get_db
from stravastats.api.models import Athlete


def test_add_athlete(app, client):
    body = {
        "strava_id": "4009189",
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "city": "Brighton",
        "country": "UK",
        "email": "testuser1@inavlid.com",
        "sex": "M",
        "weight": 75,
        "profile": "https://dgalywyr863hv.cloudfront.net/pictures/athletes/4009189/2904544/2/large.jpg",
        "created_at": 1639765803
    }

    response = client.post(
        "/athlete/add", json=body
    )
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    data = json.loads(response.data.decode())
    assert data['message'] == "Athlete 'testuser' added"

    with app.app_context():
        db = get_db()
        count = db.session.query(Athlete.id).count()
        assert count == 1


def test_get_athlete(app, client):
    with app.app_context():
        db = get_db()
        stmt = insert(Athlete).values(
            strava_id='7355260', username="test", firstname="Test",
            lastname="User 1", city="London", country="UK", email="test@invalid.com",
            sex="F", weight=100, profile="https://testurl.com/test.jpg",
            created_at=1639765803, updated_at=1639765803)
        with db.engine.connect() as conn:
            result = conn.execute(stmt)

    response = client.get("/athlete/1")
    assert response.status_code == 200
