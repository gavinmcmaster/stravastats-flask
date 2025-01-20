from flask import jsonify
from flask.wrappers import Response
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import exc
from marshmallow.exceptions import ValidationError
import time
from ..db import get_db
from .schemas import gear_schema, athlete_schema, activity_schema, auth_token_schema
from .models import AuthToken
from ..logging import Logging

class AddGearService:

    def __init__(self, json_args, _session=None, logger=Logging()) -> None:
        self.json_args = json_args
        self.session = _session or get_db().session
        self.log = logger
        
    def _get_gear(self) -> Boolean:
        try:
            self.gear = gear_schema.load(self.json_args)
            return True
        except ValidationError as error:
            self.log.log_debug(f"GearService Validation error {str(error.args[0])}")
            return False

    def process(self) -> Boolean:
        if self._get_gear():
            return True
        return False

    def save(self) -> Response:
        try:
            self.session.add(self.gear)
            self.session.commit()
            msg = jsonify({'message': f'Gear \'{self.gear.name}\' added'})
            return msg, 201
        except exc.SQLAlchemyError as error:
            self.log.log_debug(f"Error adding gear: {str(error.orig)}")
            msg = {'message': 'Error adding gear'}
            return msg, 500


class AddAthleteService:

    def __init__(self, json_args, _session=None, logger=Logging()) -> None:
        self.json_args = json_args
        self.session = _session or get_db().session
        self.log = logger

    def _get_athlete(self) -> Boolean:
        try:
            self.athlete = athlete_schema.load(self.json_args)
            return True
        except ValidationError as error:
            self.log.log_debug(f"AthleteService Validation error {str(error.args[0])}")
            return False

    def process(self) -> Boolean:
        if self._get_athlete():
            return True
        return False

    def save(self) -> Response:
        try:
            now = round(time.time())
            setattr(self.athlete, 'updated_at', now)
            self.session.add(self.athlete)
            self.session.commit()
            msg = jsonify(
                {'message': f'Athlete \'{self.athlete.username}\' added'})
            return msg, 201
        except exc.SQLAlchemyError as error:
            self.log.log_debug(f"Error adding athlete: {str(error.orig)}")
            msg = {'message': 'Error adding athlete'}
            return msg, 500


class AddActivityService:

    def __init__(self, json_args, _session=None, logger=Logging()) -> None:
        self.json_args = json_args
        self.session = _session or get_db().session
        self.log = logger

    def _get_activity(self) -> Boolean:
        try:
            self.activity = activity_schema.load(self.json_args)
            return True
        except ValidationError as error:
            self.log.log_debug(f"ActivityService Validation error {str(error.args[0])}")
            return False

    def process(self) -> Boolean:
        if self._get_activity():
            return True
        return False

    def save(self) -> Response:
        try:

            self.session.add(self.activity)
            self.session.commit()
            msg = jsonify(
                {'message': f'Activity \'{self.activity.name}\' added'})
            return msg, 201
        except exc.SQLAlchemyError as error:
            self.log.log_debug(f"Error adding activity: {str(error.orig)}")
            msg = {'message': 'Error adding activity'}
            return msg, 500


class AuthTokenService:
    def __init__(self, user_id, token, _session=None, logger=Logging()) -> None:
        self.user_id = user_id
        self.token = token
        self.session = _session or get_db().session
        self.log = logger

    def add(self) -> Boolean:
        try:
            now = round(time.time())
            data = {'user_id': self.user_id,
                    'token': self.token, 'created_at': now}
            auth_token = auth_token_schema.load(data)
            self.session.add(auth_token)
            self.session.commit()
            return True
        except exc.SQLAlchemyError as error:
            self.log.log_debug(f"Error adding token: {str(error.orig)}")
            return False

    def match(self) -> Boolean:
        try:
            auth_token = AuthToken.query.filter_by(
                user_id=self.user_id,token=self.token).first()

            return auth_token.token == self.token
        except exc.SQLAlchemyError as error:
            self.log.log_debug(f"Error matching token: {str(error.orig)}")
            return False

    def valid(self, expiry) -> Boolean:
        now = round(time.time())
        return expiry > now

    def get(self, user_id):
        try:
            auth_token = AuthToken.query.filter_by(user_id=user_id).first()
            return auth_token.token
        except exc.SQLAlchemyError as error:
            self.log.log_debug(f"Error getting token: {str(error.orig)}")
            return False

    def delete(self):
        try:
            auth_token = AuthToken.query.filter_by(
                user_id=self.user_id, token=self.token).first()
            self.session.delete(auth_token)
            self.session.commit()
            return True
        except exc.SQLAlchemyError as error:
            self.log.log_debug(f"Error deleting token: {str(error.orig)}")
            return False
