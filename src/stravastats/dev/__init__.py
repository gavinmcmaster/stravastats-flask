import click
from flask import Blueprint
from ..conf import db
import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def create_blueprint() -> Blueprint:
    bp = Blueprint("dev", __name__)

    @bp.cli.command("create-db")
    @click.option("--drop-existing", is_flag=True)
    def create_db_command(drop_existing: bool):
        uri = os.getenv('DATABASE_URI')
        engine = create_engine(uri)
        if not database_exists(engine.url):
            create_database(engine.url)
                       
        if drop_existing:
            db.drop_all()

        db.create_all()

    return bp


blueprint = create_blueprint()
