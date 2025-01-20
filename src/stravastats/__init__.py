from flask import Flask
import os
from dotenv import load_dotenv
from .dev import create_blueprint as create_dev_blueprint
from .api import create_blueprint as create_api_blueprint
from .api.auth.views import auth_blueprint
from flask_cors import CORS
from flasgger import Swagger
from . import conf
from loguru import logger

def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    CORS(app)

    load_dotenv()

    if test_config is None:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv(
            'SQL_TRACK_MODS')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    else:
        app.config.update(test_config)

    conf.db.init_app(app)
    conf.ma.init_app(app)

    app.register_blueprint(create_dev_blueprint())
    app.register_blueprint(create_api_blueprint(), url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    logger.add("data/logs/app.log", rotation="1 MB", level=os.getenv('LOG_LEVEL'))
    app.logger.addHandler(logger)

    app.secret_key = os.getenv('SECRET_KEY')

    return app

app = create_app()
swagger = Swagger(app, template={
    "info": {
        "title": "Strava Stats Flask API",
        "description": "Test API App mimicking Strava functionality, tracking athletes, activities and gears (bikes)",
        "version": "v0.2.0-alpha"
        }
    }
)
