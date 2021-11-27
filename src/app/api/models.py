from ..db import db
from sqlalchemy.sql.sqltypes import BigInteger, Float, Integer, String
from sqlalchemy import Column, ForeignKey


class Athlete(db.Model):
    id = Column(BigInteger, primary_key=True)
    strava_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False, default='')
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, default='')
    city = Column(String(100), default='')
    country = Column(String(2), default='')
    sex = Column(String(1), default='')
    weight = Column(Float(2))
    profile = Column(String(120), default='')
    time_created = Column(BigInteger, nullable=False)
    time_updated = Column(BigInteger, nullable=False)


class Gear(db.Model):
    id = Column(BigInteger, primary_key=True)
    strava_gear_id = Column(String(16), unique=True, default='')
    name = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    description = Column(String(256), default='')
    primary = Column(Integer, default=0)
    retired = Column(Integer, default=0)
    weight = Column(Float(2))


class Activity(db.Model):
    id = Column(BigInteger, primary_key=True)
    athlete_id = Column(BigInteger, ForeignKey(Athlete.id))
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
    photo_count = Column(Integer, default=0)
    average_temp = Column(Float(1))
    average_watts = Column(Float(2))
    average_speed = Column(Float(2))
    max_speed = Column(Float(2))
    calories = Column(Integer)
    bikepacking = Column(Integer, default=0)
