
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from ...db import get_db
from ..models import User
import bcrypt


class RegisterAPI(MethodView):

    def __init__(self, _session=None) -> None:
        self.session = _session or get_db().session

    def post(self):
        post_data = request.get_json()
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


class LoginAPI(MethodView):

    def __init__(self, _session=None) -> None:
        self.session = _session or get_db().session

    def post(self):
        post_data = request.get_json()
        try:

            user = User.query.filter_by(email=post_data.get('email')).first()
            if user:
                if (user.validate_credentials(post_data.get('password'))):
                    auth_token = user.encode_auth_token(user.id)
                    responseObject = {
                        'status': 'success',
                        'message': 'User successfully logged in',
                        'auth_token': auth_token
                    }
                    return make_response(jsonify(responseObject)), 200
                else:
                    return self._return_unauthorized_response()
            else:
                return self._return_unauthorized_response()
        except Exception as e:
            print("LoginAPI ERROR " + e.args[0])
            responseObject = {
                'status': 'fail',
                'message': 'An error occurred'
            }
            return make_response(jsonify(responseObject)), 500

    def _return_unauthorized_response(self):
        responseObject = {
            'status': 'fail',
            'message': 'Invalid user credentials',
        }
        return make_response(jsonify(responseObject)), 401


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')

auth_blueprint = Blueprint('auth', __name__)

# Add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
