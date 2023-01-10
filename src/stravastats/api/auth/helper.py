from functools import wraps
import os
from flask import request, make_response, jsonify
import jwt
from ..services import AuthTokenService


def validate_api_token(f):
    @wraps(f)
    def authorize(*args, **kwargs):
        if not 'Authorization' in request.headers:
            print("Bail because no Authorisation HEADER")
            return unauthorized_response()
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        # Signature expired will throw an exception
        try:
            decoded = jwt.decode(token, os.getenv('SECRET_KEY'),
                                 algorithms=['HS256'])
        except:
            return unauthorized_response()
        user_id = decoded['sub']
        token_service = AuthTokenService(user_id, token)
        # TODO Handle refresh token here? JWT extended?
        if not token_service.match():
            print(
                f"Validate API Token ERROR - No matching token found for user id {user_id}")
            return unauthorized_response()

        if not token_service.valid(decoded['exp']):
            print(
                f"Validate API Token ERROR - Token expired")
            return unauthorized_response()            

        return f(*args, **kwargs)
    return authorize


def unauthorized_response():
    responseObject = {
        'status': 'fail',
        'message': 'Not authorized',
    }
    return make_response(jsonify(responseObject)), 401
