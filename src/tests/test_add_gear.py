from app import create_app
import json


def test_add_gear():
    with create_app().test_client() as client:
        # INSTALL
        # https://pypi.org/project/pytest-flask-sqlalchemy/
        # A pytest plugin for preserving test isolation in Flask-SQlAlchemy using database transactions.
        gear = {}
        gear['name'] = "Test Gear Name"
        gear['brand_name'] = "Test Gear Brand Name"
        gear['model_name'] = "Test Gear Model Name"

        res = client.post(
            '/gear/add',
            data=json.dumps(gear),
            headers={"Content-Type": "application/json"}
        )

        assert res.status_code == 201
        #gear_name = gear['name']
        #assert res.data['message'] == f'Gear \'{gear_name}\' added'
