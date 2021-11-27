from flask import Blueprint
#from sqlalchemy import exc
#from sqlalchemy.orm.session import Session
# from ..db import db, get_or_create,
#import json
from .controllers import Routes


def create_blueprint() -> Blueprint:
    bp = Blueprint('api', __name__)
    routes = Routes(bp)
    bp = routes.get_blueprint()
    return routes.bp


blueprint = create_blueprint()
