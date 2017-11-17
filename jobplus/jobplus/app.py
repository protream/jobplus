from flask import Flask
from jobplus.config import configs
from jobplus.models import db, User, Delivery
from flask_migrate import Migrate


def register_blueprints(app):
    from .handlers import front
    app.register_blueprint(front)


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extensions(app)
    register_blueprints(app)
    return app
