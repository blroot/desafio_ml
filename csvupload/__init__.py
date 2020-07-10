from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from config import Config
from StreamParserFactory import StreamParserFactory
from CsvParser import CsvParser

db = SQLAlchemy()
celery = Celery(broker=Config.CELERY_BROKER_URL)
parser_factory = StreamParserFactory()
parser_factory.register_parser('csv', CsvParser)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    celery.conf.update(app.config)

    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

        return app
