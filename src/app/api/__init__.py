from flask import Blueprint
from .controllers import Routes


def create_blueprint() -> Blueprint:
    bp = Blueprint('api', __name__)
    routes = Routes(bp)
    bp = routes.get_blueprint()
    return routes.bp


blueprint = create_blueprint()
