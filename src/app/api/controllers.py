from flask import Blueprint, request
from flask.json import jsonify
from sqlalchemy import exc
from .models import Athlete, Activity, Gear
from .schemas import athlete_schema, gears_schema, activities_schema
from .services import AddActivityService, AddGearService, AddAthleteService


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
        def add_athlete():
            service = AddAthleteService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_add_activity(self):
        @self.bp.route('/activity/add', methods=['POST'])
        def add_activity():
            service = AddActivityService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_add_gear(self):
        @self.bp.route('/gear/add', methods=['POST'])
        def add_gear():
            service = AddGearService(json_args=request.get_json())
            if service.process():
                return service.save()

            msg = jsonify({'message': 'Bad Request'})
            return msg, 400

    def route_get_gears(self):
        @self.bp.route('/gears', methods=['GET'])
        def get_gears():
            gears = Gear.query.all()
            if gears is not None:
                response = jsonify(gears_schema.dump(gears))
                return response, 200

            msg = {'message': 'No gears found'}
            return msg, 400

    def route_get_athlete(self):
        @self.bp.route('/athlete/<id>', methods=['GET'])
        def get_athlete(id):
            athlete = Athlete.query.get(id)
            if athlete is not None:
                response = jsonify(athlete_schema.dump(athlete))
                return response, 200

            msg = {'message': 'Error, athlete not found'}
            return msg, 400

    def route_get_activities(self):
        @self.bp.route('/activities/<athleteid>', methods=['GET'])
        def get_activities(athleteid):
            activities = Activity.query.filter(
                Activity.athlete_id == athleteid).all()

            if len(activities) > 0:
                response = jsonify(activities_schema.dump(activities))
                return response, 200

            msg = {'message': 'No activities found'}
            return msg, 400


'''
    def route_update_athlete(self):
        @self.bp.route('/athlete/update/<id>', methods=['POST'])
        def update_athlete(id):
            session = db.session
            data = request.get_json()
            immutable_fields = ['id', 'strava_id',
                                'username', 'time_created', 'time_updated']
            athlete_id = id
            existing = session.query(Athlete).filter_by(id=athlete_id).first()
            if existing is None:
                msg = {'message': 'Error updating athlete, record not found'}
                return msg, 400

            update_list = list(set(data) - set(immutable_fields))
            update_values = {}
            for key in update_list:
                v = data.get(key)
                e = existing.__getattribute__(key)
                print(f'new {v}, compare with existing {e}')
                if v != e:
                    update_values[key] = v

            if len(update_values) > 0:
                update_values['time_updated'] = round(time.time())
                try:
                    session.query(Athlete).filter_by(
                        id=existing.id).update(update_values)
                    session.commit()
                    msg = {
                        'message': f'Athlete {existing.username} successfully updated!'}
                    return msg, 200
                except exc.SQLAlchemyError as error:
                    print("ERROR: " + str(error.orig))
                    msg = {'message': 'Error updating athlete'}
                    return msg, 500
            else:
                msg = {'message': 'Athlete already up to date'}
                return msg, 200
'''
