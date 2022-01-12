
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from ...db import get_db
from ..models import User


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def __init__(self, _session=None) -> None:
        self.session = _session or get_db().session

    def post(self):
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    strava_id=post_data.get('strava_id')
                )
                self.session.add(user)
                self.session.commit()
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'User successfully registered',
                    'auth_token': auth_token
                }

                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                print("RegisterAPI ERROR " + str(e.args[0]))
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
auth_blueprint = Blueprint('auth', __name__)

# Add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
