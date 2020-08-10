from flask_marshmallow import Marshmallow
from flask_uuid import FlaskUUID
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager



db = SQLAlchemy()
ma = Marshmallow()
flask_uuid = FlaskUUID()
jwt=JWTManager()
