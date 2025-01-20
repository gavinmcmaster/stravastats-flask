
from flask import Blueprint, request, jsonify, make_response, session
from flask.views import MethodView
from ...db import get_db
from ..models import User
from .helper import validate_api_token, unauthorized_response
from ..services import AuthTokenService
from flasgger.utils import swag_from
from ..schema_docs import register_user_dict, user_login_dict
from ...logging import Logging

class RegisterAPI(MethodView):

    def __init__(self, _session=None) -> None:
        self.session = _session or get_db().session
        self.log = Logging()

    @swag_from(register_user_dict)
    def post(self):
        """
        Register user
        ---
        """
        post_data = request.get_json()
        # Email & password are required
        #TODO validate email
        if not (post_data.get('email') and post_data.get('password')):
            responseObject = {
                'status': 'fail',
                'message': 'Invalid data.'
            }
            return make_response(jsonify(responseObject)), 400

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
                token_service = AuthTokenService(user.id, auth_token)
                if not token_service.add():
                    return unauthorized_response()

                response = jsonify({
                    'status': 'success',
                    'message': 'User successfully registered',
                    'auth_token': auth_token
                });

                return response, 201

            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'An internal error occurred'
                }
                return make_response(jsonify(responseObject)), 500
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists',
            }
            return make_response(jsonify(responseObject)), 409


class LoginAPI(MethodView):

    def __init__(self, _session=None) -> None:
        self.session = _session or get_db().session

    @swag_from(user_login_dict)
    def post(self):
        """
        User login
        ---
        """
        post_data = request.get_json()
        # Email & password are required
        #TODO validate email
        if not (post_data.get('email') and post_data.get('password')):
            responseObject = {
                'status': 'fail',
                'message': 'Invalid data.'
            }
            return make_response(jsonify(responseObject)), 400
        try:

            user = User.query.filter_by(email=post_data.get('email')).first()
            if user:
                if (user.validate_credentials(post_data.get('password'))):
                    auth_token = user.encode_auth_token(user.id)
                    token_service = AuthTokenService(user.id, auth_token)
                    if not token_service.add():
                        return unauthorized_response()
                    responseObject = {
                        'status': 'success',
                        'message': 'User successfully logged in',
                        'auth_token': auth_token
                    }
                    session['user_id'] = user.id

                    return make_response(jsonify(responseObject)), 200
                else:
                    return unauthorized_response()
            else:

                return unauthorized_response()
        except Exception as e:
            self.log.log_debug(f"LoginAPI ERROR {str(e.args[0])}")
            responseObject = {
                'status': 'fail',
                'message': 'An error occurred'
            }
            return make_response(jsonify(responseObject)), 500


class LogoutAPI(MethodView):

    def __init__(self, _session=None) -> None:
        self.session = _session or get_db().session

    @validate_api_token
    def post(self):
        """
        User logout
        ---
        tags:
            - Authentication
        description: Logs out currently logged-in user
        responses:
            200:
                description: 'Successfully logged out'
            400:
                description: 'Not authorized'
            500:
                description: 'An internal error occurred'
        """
        try:
            token = self._get_token()
            user_id = session['user_id']
            token_service = AuthTokenService(user_id, token)
            if not token_service.delete():
                return unauthorized_response()

            session['user_id'] = None
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged out'
            }
            return make_response(jsonify(responseObject)), 200
        except:
            responseObject = {
                'status': 'fail',
                'message': 'An internal error occurred',
            }
        return make_response(jsonify(responseObject)), 500

    def _get_token(self) -> str:
        data = request.headers['Authorization']
        return str.replace(str(data), 'Bearer ', '')


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')

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

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
