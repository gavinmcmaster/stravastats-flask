from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

from .dev import create_blueprint as create_dev_blueprint
from .db import db
from .api import create_blueprint as create_api_blueprint


def create_app() -> Flask:
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQL_TRACK_MODS')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

    SQLAlchemy.init_app(db, app)

    app.register_blueprint(create_dev_blueprint())
    app.register_blueprint(create_api_blueprint())

    return app


app = create_app()
