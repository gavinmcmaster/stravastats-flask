from xmlrpc.client import Boolean
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, Float, Integer, String
import jwt
import bcrypt
import os
import time
import datetime
from ..conf import db


class Athlete(db.Model):
    id = Column(BigInteger, primary_key=True)
    strava_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, default='')
    city = Column(String(100), default='')
    country = Column(String(2), default='')
    sex = Column(String(1), default='')
    weight = Column(Float(2))
    profile = Column(String(120), default='')
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)


class User(db.Model):
    # Table can't be called 'user' in Postgresql
    __tablename__ = "registered_user"

    id = Column(BigInteger, primary_key=True)
    email = Column(String(100), nullable=False, default='')
    password = db.Column(db.String(255), nullable=False)
    strava_id = Column(BigInteger, ForeignKey(
        Athlete.strava_id), unique=True, nullable=True)
    created_at = Column(BigInteger, nullable=False)

    def __init__(self, email, password, strava_id=None) -> None:
        self.email = email
        encoded_pass = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(encoded_pass, salt).decode()
        self.strava_id = strava_id
        self.created_at = round(time.time())

    def validate_credentials(self, password) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        except Exception as e:
            # log exception
            return False

    def encode_auth_token(self, user_id) -> String:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }

        return jwt.encode(
            payload,
            os.getenv('SECRET_KEY'),
            algorithm='HS256'
        )


class Gear(db.Model):
    id = Column(BigInteger, primary_key=True)
    strava_gear_id = Column(String(16), unique=True)
    name = Column(String(100), nullable=False)
    brand_name = Column(String(100), nullable=False)
    model_name = Column(String(100), nullable=False)
    description = Column(String(256), default='')
    primary = Column(Integer, default=0)
    retired = Column(Integer, default=0)
    weight = Column(Float(2))
    created_at = Column(BigInteger, nullable=False)


class Activity(db.Model):
    id = Column(BigInteger, primary_key=True)
    athlete_id = Column(BigInteger)
    name = Column(String(100), nullable=False)
    description = Column(String(256), default='')
    distance = Column(Integer, nullable=False)
    moving_time = Column(Integer, nullable=False)
    elapsed_time = Column(Integer, nullable=False)
    elevation_gain = Column(Integer, default=0)
    gear_id = Column(BigInteger, ForeignKey(Gear.id))
    start_date = Column(BigInteger, nullable=False)
    start_latitude = Column(Float(6))
    start_longitude = Column(Float(6))
    strava_ride_id = Column(BigInteger, unique=True, default=0)
    achievement_count = Column(Integer, default=0)
    kudos_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    pr_count = Column(Integer, default=0)
    photo_count = Column(Integer, default=0)
    average_temp = Column(Float(1))
    average_watts = Column(Float(2))
    average_speed = Column(Float(2))
    max_speed = Column(Float(2))
    calories = Column(Integer)
    bikepacking = Column(Integer, default=0)


class AuthToken(db.Model):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    token = Column(String(200), nullable=False)
    created_at = Column(BigInteger, nullable=False)
