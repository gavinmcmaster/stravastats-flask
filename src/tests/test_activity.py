import json
from sqlalchemy import insert
from stravastats.db import get_db
from stravastats.api.models import Activity


def test_add_activity(app, client, login):
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
        "/activity/add", json=body,
        headers=dict(
            Authorization='Bearer ' + login['auth_token']
        )
    )
    assert response.status_code == 201
    assert response.content_type == 'application/json'
    data = json.loads(response.data.decode())
    assert data['message'] == "Activity 'NC500: Brora to Dingwall' added"

    with app.app_context():
        db = get_db()
        count = db.session.query(Activity.id).count()
        assert count == 1


def test_get_activity(app, client, login):
    with app.app_context():
        db = get_db()
        stmt = insert(Activity).values(athlete_id=4009176, name="NC500: Brora to Dingwall",
                                       distance=107254, moving_time=19701, elapsed_time=27556, elevation_gain=750,
                                       start_date=1640013750, kudos_count=18, comment_count=2, photo_count=0,
                                       description="It doesn't take much of a hill to put me in the small ring now",
                                       calories=2884, average_speed=5.444, max_speed=14.5, pr_count=0, average_temp=12)
        with db.engine.connect() as conn:
            result = conn.execute(stmt)

        response = client.get("/activities/4009176",
                              headers=dict(
                                  Authorization='Bearer ' + login['auth_token']
                              ))
        assert response.status_code == 200


def test_get_no_activities(app, client, login):
    with app.app_context():
        db = get_db()
        stmt = insert(Activity).values(athlete_id=5009176, name="NC500: Brora to Dingwall",
                                       distance=107254, moving_time=19701, elapsed_time=27556, elevation_gain=750,
                                       start_date=1640013750, kudos_count=18, comment_count=2, photo_count=0,
                                       description="It doesn't take much of a hill to put me in the small ring now",
                                       calories=2884, average_speed=5.444, max_speed=14.5, pr_count=0, average_temp=12)
        with db.engine.connect() as conn:
            result = conn.execute(stmt)

        response = client.get("/activities/4009176",
                              headers=dict(
                                  Authorization='Bearer ' + login['auth_token']
                              ))
        data = json.loads(response.data.decode())
        assert data['message'] == 'No activities found for this athlete'
        assert response.status_code == 400
