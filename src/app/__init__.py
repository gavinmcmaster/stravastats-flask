from flask import Flask
import os
from dotenv import load_dotenv
from .dev import create_blueprint as create_dev_blueprint
from .api import create_blueprint as create_api_blueprint
from .conf import ma, db


def create_app() -> Flask:
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQL_TRACK_MODS')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(create_dev_blueprint())
    app.register_blueprint(create_api_blueprint())

    return app


app = create_app()
