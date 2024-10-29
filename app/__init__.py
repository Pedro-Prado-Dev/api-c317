from flask import Flask
from app.config import Config
from app.extensions import db, migrate, api
from app.users.routes import UserResource
from app.group.routes import GroupUserResource, GroupResource, GroupListResource
from app.form.routes import FormComponentResource, FormResource, ComponentOptionResource


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    return app
