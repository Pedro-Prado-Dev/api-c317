from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import api, db, migrate
from app.form.routes import ComponentOptionResource, FormComponentResource, FormResource
from app.group.routes import GroupListResource, GroupResource, GroupUserResource
from app.users.routes import UserResource


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    CORS(app)

    return app
