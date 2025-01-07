from flask import Blueprint, request
from flask.json import jsonify
from .models import Athlete, Activity, Gear
from .schemas import athlete_schema, gears_schema, activities_schema
from .services import AddActivityService, AddGearService, AddAthleteService
from .auth.helper import validate_api_token
import os
from sqlalchemy import exc
from flasgger.utils import swag_from
from .schema_docs import add_activity_dict, add_athlete_dict, get_athlete_dict, get_activities_dict, add_gear_dict, get_gears_dict

class Routes:

    def __init__(self, bp: Blueprint) -> None:
        self.bp = bp

    def get_blueprint(self) -> Blueprint:
        self.route_add_home()
        self.route_add_athlete()
        self.route_add_activity()
        self.route_add_gear()
        self.route_get_athlete()
        self.route_get_gears()
        self.route_get_activities()
        self.route_get_strava_app()

        return self.bp

    def route_add_home(self):
        @self.bp.route('/', methods=['GET'])
        def add_home():
            """
            API App homepage
            ---
            tags:
                - Home
            description: Returns message showing app is up.
            responses:
                200:
                    description: A successful response
                    examples:
                        application/json: "Strava Stats API App is running!"
            """
            msg = "Strava Stats API App is running!"
            status_code = 200
            return msg, status_code

    def route_add_athlete(self):
        @swag_from(add_athlete_dict)
        @self.bp.route('/athlete/add', methods=['POST'])
        @validate_api_token
        def add_athlete():
            """
            Add new Strava athlete profile
            ---
            """
            service = AddAthleteService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_add_activity(self):
        @swag_from(add_activity_dict)
        @self.bp.route('/activity/add', methods=['POST'])
        @validate_api_token
        def add_activity():
            """
            Add new Strava actity
            ---
            """
            service = AddActivityService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_add_gear(self):
        @swag_from(add_gear_dict)
        @self.bp.route('/gear/add', methods=['POST'])
        @validate_api_token
        def add_gear():
            """
            Add new bike
            ---
            """
            service = AddGearService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_get_gears(self):
        @swag_from(get_gears_dict)
        @self.bp.route('/gears', methods=['GET'])
        @validate_api_token
        def get_gears():
            """
            List all bikes
            ---
            """
            try:
                gears = Gear.query.all()
                response = jsonify(gears_schema.dump(gears))
                return response, 200
            except exc.SQLAlchemyError as error:
                msg = {'message': 'An internal error occurred'}
                return msg, 500

    def route_get_athlete(self):
        @swag_from(get_athlete_dict)
        @self.bp.route('/athlete/<id>', methods=['GET'])
        @validate_api_token
        def get_athlete(id):
            """
            Fetch athlete profile given its identifier
            ---
            """
            athlete = Athlete.query.get(id)
            if athlete is not None:
                response = jsonify(athlete_schema.dump(athlete))
                return response, 200

            msg = {'message': 'Error, athlete not found'}
            return msg, 400

    def route_get_activities(self):
        @swag_from(get_activities_dict)
        @self.bp.route('/activities/<athleteid>', methods=['GET'])
        @validate_api_token
        def get_activities(athleteid):
            """
            Fetch activities for a given athlete strava id
            ---
            """
            try:
                activities = Activity.query.filter(
                Activity.athlete_id == athleteid).all()
                response = jsonify(activities_schema.dump(activities))
                return response, 200
            except exc.SQLAlchemyError as error:
                msg = {'message': 'An internal error occurred'}
                return msg, 500

    def route_get_strava_app(self):
        @self.bp.route('/strava/app/key', methods=['GET'])
        @validate_api_token
        def get_strava_app():
            """
            Strava
            ---
            tags:
                - Strava
            description: Returns Strava Credentials
            responses:
                200:
                    description: JSON object containing Strava credentials
                    examples:
                        application/json: {strava_client_id: string, strava_client_secret: string}
            """
            responseObject = {
                'strava_client_id': os.getenv('STRAVA_CLIENT_ID'),
                'strava_client_secret': os.getenv('STRAVA_CLIENT_SECRET')
            }
            return jsonify(responseObject), 200
