from stravastats.db import get_db
from stravastats.api.models import Activity
from sqlalchemy import insert
from .conftest import decode_response


def test_add_activity(app, client):
    body = {
        "athlete_id": 4009189,
        "name": "NC500: Brora to Dingwall",
        "distance": 107254,
        "moving_time": 19701,
        "elapsed_time": 27556,
        "elevation_gain": 750,
        "start_date": 1640013750,
        "start_latitude": 58.012933,
        "start_longitude": -4.425155,
        "achievement_count": 0,
        "kudos_count": 18,
        "comment_count": 2,
        "photo_count": 0,
        "description": "It doesn't take much of a hill to put me in the small ring now",
        "calories": 2884,
        "average_speed": 5.444,
        "max_speed": 14.5,
        "pr_count": 0,
        "average_temp": 12,
        "bikepacking": 1
    }

    response = client.post(
        "/activity/add", json=body
    )
    assert response.status_code == 201
    data = decode_response(response.data)
    assert data['message'] == "Activity 'NC500: Brora to Dingwall' added"

    with app.app_context():
        db = get_db()
        count = db.session.query(Activity.id).count()
        assert count == 1


def test_get_activity(app, client):
    with app.app_context():
        db = get_db()
        stmt = insert(Activity).values(athlete_id=4009176, name="NC500: Brora to Dingwall",
                                       distance=107254, moving_time=19701, elapsed_time=27556, elevation_gain=750,
                                       start_date=1640013750, kudos_count=18, comment_count=2, photo_count=0,
                                       description="It doesn't take much of a hill to put me in the small ring now",
                                       calories=2884, average_speed=5.444, max_speed=14.5, pr_count=0, average_temp=12)
        with db.engine.connect() as conn:
            result = conn.execute(stmt)

        response = client.get("/activities/4009176")
        assert response.status_code == 200
