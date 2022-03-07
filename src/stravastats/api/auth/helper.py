from functools import wraps
import os
from flask import request, abort, make_response, jsonify
import jwt
from ..services import AuthTokenService


def validate_api_token(f):
    @wraps(f)
    def authorize(*args, **kwargs):
        if not 'Authorization' in request.headers:
            print("Bail because no Authorisation HEADER")
            abort(401)
        data = request.headers['Authorization']
        token = str.replace(str(data), 'Bearer ', '')
        # Signature expired will throw an exception
        decoded = jwt.decode(token, os.getenv('SECRET_KEY'),
                             algorithms=['HS256'])
        user_id = decoded['sub']
        token_service = AuthTokenService(user_id, token)
        # TODO Handle refresh token here?
        if not token_service.match():
            print(
                f"Validate API Token ERROR - No matching token found for user id {user_id}")
            abort(401)

        return f(*args, **kwargs)
    return authorize


def unauthorized_response():
    responseObject = {
        'status': 'fail',
        'message': 'Invalid user credentials',
    }
    return make_response(jsonify(responseObject)), 401
