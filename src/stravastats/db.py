from flask_sqlalchemy import SQLAlchemy
from .conf import db


def get_db() -> SQLAlchemy:
    return db


def reset_db():
    drop_db()
    db.create_all()


def drop_db():
    db.drop_all
