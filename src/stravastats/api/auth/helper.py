from functools import wraps
import os
from flask import request, make_response, jsonify
import jwt
from ..services import AuthTokenService
from ...logging import Logging

def validate_api_token(f):
    @wraps(f)
    def authorize(*args, **kwargs):
        if not 'Authorization' in request.headers:
            Logging().reqest_error("No Authorisation HEADER", request)
            return unauthorized_response()
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        # Signature expired will throw an exception
        try:
            decoded = jwt.decode(token, os.getenv('SECRET_KEY'),
                                 algorithms=['HS256'])
        except Exception as e:
            return unauthorized_response()
        user_id = decoded['sub']
        token_service = AuthTokenService(user_id, token)
        # TODO Handle refresh token here? JWT extended?
        if not token_service.match():
            Logging().log_debug(f"Token {token} not found for user {user_id}")
            return unauthorized_response()

        if not token_service.valid(decoded['exp']):
            Logging().log_debug(f"Token {token} expired")
            return unauthorized_response()            

        return f(*args, **kwargs)
    return authorize


def unauthorized_response():
    responseObject = {
        'status': 'fail',
        'message': 'Not authorized',
    }
    return make_response(jsonify(responseObject)), 401
