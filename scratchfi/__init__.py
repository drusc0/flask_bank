import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # @app.teardown_appcontext
    # def remove_db():
    #     db.drop_all()

    with app.app_context():
        initialize_extensions(app)
        return app


def initialize_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    from scratchfi import routes, models, db_setup
    db_setup.init_db()
