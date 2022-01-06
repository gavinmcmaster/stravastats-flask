from flask import jsonify
from flask.wrappers import Response
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import exc
from marshmallow.exceptions import ValidationError
import time
from ..conf import db
from .schemas import gear_schema, athlete_schema, activity_schema


class AddGearService:

    def __init__(self, json_args, _session=None) -> None:
        self.json_args = json_args
        self.session = _session or db.session

    def _get_gear(self) -> Boolean:
        try:
            self.gear = gear_schema.load(self.json_args)
            return True
        except ValidationError as error:
            print("GearService Validation error " + str(error.args[0]))
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
            print("ERROR: " + str(error.orig))
            msg = {'message': 'Error adding gear'}
            return msg, 500


class AddAthleteService:

    def __init__(self, json_args, _session=None) -> None:
        self.json_args = json_args
        self.session = _session or db.session

    def _get_athlete(self) -> Boolean:
        try:
            self.athlete = athlete_schema.load(self.json_args)
            return True
        except ValidationError as error:
            print("AthleteService Validation error " + str(error.args[0]))
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
            print("ERROR: " + str(error.orig))
            msg = {'message': 'Error adding athlete'}
            return msg, 500


class AddActivityService:

    def __init__(self, json_args, _session=None) -> None:
        self.json_args = json_args
        self.session = _session or db.session

    def _get_activity(self) -> Boolean:
        try:
            self.activity = activity_schema.load(self.json_args)
            return True
        except ValidationError as error:
            print("AthleteService Validation error " + str(error.args[0]))
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
            print("ERROR: " + str(error.orig))
            msg = {'message': 'Error adding activity'}
            return msg, 500
