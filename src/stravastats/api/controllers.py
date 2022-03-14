import os
from flask import Blueprint, request
from flask.json import jsonify
from .models import Athlete, Activity, Gear
from .schemas import athlete_schema, gears_schema, activities_schema
from .services import AddActivityService, AddGearService, AddAthleteService
from .auth.helper import validate_api_token


class Routes:

    def __init__(self, bp: Blueprint) -> None:
        self.bp = bp

    def get_blueprint(self) -> Blueprint:
        self.route_add_athlete()
        self.route_add_activity()
        self.route_add_gear()
        self.route_get_athlete()
        self.route_get_gears()
        self.route_get_activities()
        # self.route_update_athlete()

        return self.bp

    def route_add_athlete(self):
        @self.bp.route('/athlete/add', methods=['POST'])
        @validate_api_token
        def add_athlete():
            service = AddAthleteService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_add_activity(self):
        @self.bp.route('/activity/add', methods=['POST'])
        @validate_api_token
        def add_activity():
            service = AddActivityService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_add_gear(self):
        @self.bp.route('/gear/add', methods=['POST'])
        @validate_api_token
        def add_gear():
            service = AddGearService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_get_gears(self):
        @self.bp.route('/gears', methods=['GET'])
        @validate_api_token
        def get_gears():
            gears = Gear.query.all()
            if gears is not None:
                response = jsonify(gears_schema.dump(gears))
                return response, 200

            msg = {'message': 'No gears found'}
            return msg, 400

    def route_get_athlete(self):
        @self.bp.route('/athlete/<id>', methods=['GET'])
        @validate_api_token
        def get_athlete(id):
            athlete = Athlete.query.get(id)
            if athlete is not None:
                response = jsonify(athlete_schema.dump(athlete))
                return response, 200

            msg = {'message': 'Error, athlete not found'}
            return msg, 400

    def route_get_activities(self):
        @self.bp.route('/activities/<athleteid>', methods=['GET'])
        @validate_api_token
        def get_activities(athleteid):
            activities = Activity.query.filter(
                Activity.athlete_id == athleteid).all()

            if len(activities) > 0:
                response = jsonify(activities_schema.dump(activities))
                return response, 200

            msg = {'message': 'No activities found for this athlete'}
            return msg, 400
