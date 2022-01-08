from flask import Flask
import os
from dotenv import load_dotenv
from .dev import create_blueprint as create_dev_blueprint
from .api import create_blueprint as create_api_blueprint
from .conf import ma, db


def create_app(testing=None) -> Flask:
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv(
        'SQL_TRACK_MODS')

    if testing is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_UNIT_TEST_URI')

    conf.db.init_app(app)
    conf.ma.init_app(app)

    app.register_blueprint(create_dev_blueprint())
    app.register_blueprint(create_api_blueprint())

    return app


app = create_app()
