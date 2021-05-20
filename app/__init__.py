from flask import Flask
from flask_restful import Api

from app.db import db
from app.ext import ma, migrate
from app.payments.api_v1.resources import payment_v1_0_bp


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    # Init the extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    # Register all 404 errors
    Api(app, catch_all_404s=True)
    # Turn off strict end URL /
    app.url_map.strict_slashes = False
    # Register the blueprints
    app.register_blueprint(payment_v1_0_bp)
    return app
