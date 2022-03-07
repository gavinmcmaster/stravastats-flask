from .models import Athlete, Gear, Activity, AuthToken
from ..conf import ma


class AthleteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Athlete
        load_instance = True
        fields = ("strava_id", "username", "firstname", "lastname", "city", "country",
                  "email", "sex", "weight", "profile", "created_at")


athlete_schema = AthleteSchema()
athletes_schema = AthleteSchema(many=True)


class GearSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Gear
        load_instance = True


gear_schema = GearSchema()
gears_schema = GearSchema(many=True)


class ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity
        load_instance = True
        # Need to work out gear id & athlete id (from strava values), convert start time
        '''fields = ("athlete_id", "name", "distance", "moving_time", "elapsed_time", "start_date", "start_latitude",
                  "start_longitude", "achievement_count", "kudos_count", "comment_count",
                  "photo_count", "pr_count", "description", "calories", "average_speed", "max_speed",
                  "average_watts", "average_temp", "bikepacking", "elevation_gain")
        '''


activity_schema = ActivitySchema()
activities_schema = ActivitySchema(many=True)


class AuthTokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthToken
        load_instance = True
        include_fk = True


auth_token_schema = AuthTokenSchema()
