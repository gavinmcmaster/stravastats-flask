from flask import Blueprint, request
from sqlalchemy import exc
from sqlalchemy.orm import session
import time
from dateutil.parser import parse
from dateutil.tz import tzutc
from .models import Athlete, Activity, Gear
from ..db import db


class Routes:

    def __init__(self, bp: Blueprint) -> None:
        self.bp = bp

    def get_blueprint(self) -> Blueprint:
        self.route_add_athlete()
        self.route_add_activity()
        self.route_add_gear()
        # TODO add get & update routes for each
        self.route_get_athlete()
        self.route_update_athlete()

        return self.bp

    def route_add_athlete(self):
        @self.bp.route('/athlete/add', methods=['POST'])
        def add_athlete():
            data = request.get_json()
            try:
                stravaid = data['strava_id']
                username = data['username']
                firstname = data['firstname']
                lastname = data['lastname']
                email = data['email']
            except KeyError as error:
                print("ERROR: Missing arg " + error.args[0])
                msg = {'message': 'Error adding athlete, missing required field'}
                return msg, 400

            session = db.session
            instance = session.query(Athlete).filter_by(
                strava_id=stravaid).first()
            if instance:
                msg = {'message': 'Error, User already exists'}
                return msg, 400

            city = data.get('city', '')
            country = data.get('country', '')
            weight = data.get('weight', '')
            profile = data.get('profile', '')
            sex = data.get('sex', '')
            now = round(time.time())

            athlete = Athlete(
                strava_id=stravaid,
                username=username,
                firstname=firstname,
                lastname=lastname,
                email=email,
                city=city,
                country=country,
                weight=weight,
                profile=profile,
                sex=sex,
                time_created=now,
                time_updated=now
            )

            try:
                session.add(athlete)
                session.commit()
                msg = {'message': f'User {athlete.username} added'}
                return msg, 200
            except exc.SQLAlchemyError as error:
                print("ERROR: " + str(error.orig))
                msg = {'message': 'Error adding user'}
                return msg, 500

    def route_add_activity(self):
        @self.bp.route('/activity/add', methods=['POST'])
        def add_activity():
            session = db.session
            data = request.get_json()
            try:
                strava_athlete_id = data['strava_athlete_id']
                name = data['name']
                distance = data['distance']
                moving_time = data['moving_time']
                elapsed_time = data['elapsed_time']
                # Arrives in Java ZonedDateTime format e.g '2021-09-11T08:33:11Z'
                start_date = round(parse(data['start_date_local'],
                                   fuzzy_with_tokens=True)[0].timestamp())
                average_speed = round(data['average_speed'], 2)
                max_speed = round(data['max_speed'], 2)
            except KeyError:
                msg = {'message': 'Error adding activity, missing required field'}
                return msg, 400

            athlete = session.query(Athlete).filter_by(
                strava_id=strava_athlete_id).first()
            if athlete is None:
                msg = {'message': 'Error adding activity, athlete not registered'}
                return msg, 400

            strava_ride_id = data.get('id', 0)
            existing = session.query(Activity).filter_by(
                strava_ride_id=strava_ride_id).first()
            if existing is not None:
                msg = {'message': 'Error, activity already registered'}
                return msg, 400

            gear_id = data.get('gear_id', None)
            if gear_id is not None:
                gear = session.query(Gear).filter_by(
                    strava_gear_id=gear_id).first()
                gear_id = gear.id
            description = data.get('description', '')
            start_latitude = data.get('start_latitude', 0)
            start_longitude = data.get('start_longitude', 0)
            achievement_count = data.get('achievement_count', 0)
            kudos_count = data.get('kudos_count', 0)
            comment_count = data.get('comment_count', 0)
            photo_count = data.get('photo_count', 0)
            average_watts = data.get('average_watts', 0)
            average_temp = data.get('average_temp', 0)
            calories = data.get('calories', 0)
            bikepacking = data.get('bikepacking', 0)
            elevation_gain = data.get('total_elevation_gain', 0)
            average_speed = round(data.get('average_speed', 0), 2)
            max_speed = round(data.get('average_speed', 0), 2)

            activity = Activity(
                athlete_id=athlete.id,
                name=name,
                description=description,
                distance=distance,
                moving_time=moving_time,
                elapsed_time=elapsed_time,
                elevation_gain=elevation_gain,
                gear_id=gear_id,
                start_date=start_date,
                start_latitude=start_latitude,
                start_longitude=start_longitude,
                strava_ride_id=strava_ride_id,
                achievement_count=achievement_count,
                kudos_count=kudos_count,
                comment_count=comment_count,
                photo_count=photo_count,
                average_temp=average_temp,
                average_watts=average_watts,
                calories=calories,
                bikepacking=bikepacking
            )

            try:
                session.add(activity)
                session.commit()
                msg = {'message': f'Activity \'{activity.name}\' added'}
                return msg, 200
            except exc.SQLAlchemyError as error:
                print("ERROR: " + str(error.orig))
                msg = {'message': 'Error adding activity'}
                return msg, 500

    def route_add_gear(self):
        @self.bp.route('/gear/add', methods=['POST'])
        def add_gear():
            session = db.session
            data = request.get_json()
            try:
                name = data['name']
                brand = data['brand_name']
                model = data['model_name']
            except KeyError as error:
                print("ERROR: Missing arg " + error.args[0])
                msg = {'message': 'Error adding gear, missing required field'}
                return msg, 400

            strava_gear_id = data.get('id', 'Not set')
            existing = session.query(Gear).filter_by(
                strava_gear_id=strava_gear_id).first()
            if existing is not None and existing.strava_gear_id != 'Not set':
                msg = {'message': 'Error, gear already registered'}
                return msg, 400

            description = data.get('description', '')
            primary = int(data.get('primary', 0))
            retired = int(data.get('retired', 0))
            weight = data.get('weight', 0)

            gear = Gear(
                strava_gear_id=strava_gear_id,
                name=name,
                brand=brand,
                model=model,
                description=description,
                primary=primary,
                retired=retired,
                weight=weight
            )

            try:
                session.add(gear)
                session.commit()
                msg = {'message': f'Gear \'{gear.name}\' added'}
                return msg, 200
            except exc.SQLAlchemyError as error:
                print("ERROR: " + str(error.orig))
                msg = {'message': 'Error adding gear'}
                return msg, 500

    def route_get_athlete(self):
        @self.bp.route('/athlete/<id>', methods=['GET'])
        def get_athlete(id):
            session = db.session
            athlete = session.query(Athlete).filter_by(
                id=id).first()

            if athlete is not None:
                data = {'strava_id': athlete.strava_id, 'firstname': athlete.firstname,
                        'lastname': athlete.lastname, 'profile': athlete.profile, 'sex': athlete.sex,
                        'city': athlete.city, 'country': athlete.country, 'email': athlete.email,
                        'weight': athlete.weight, 'created_at': athlete.time_created,
                        'updated_at': athlete.time_updated}
                return data, 200

            msg = {'message': 'Error, athlete not found'}
            return msg, 400

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
