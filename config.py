from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    # App config
    FILE_PATH = environ.get('FILE_PATH')
    FILE_TYPE = environ.get('FILE_TYPE')
    DELIMITER = environ.get('DELIMITER')
    RECORD_POOL_SIZE = int(environ.get("RECORD_POOL_SIZE"))
    ASYNC_REQUESTS_SEMAPHORE = int(environ.get("ASYNC_REQUESTS_SEMAPHORE"))

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery
    CELERY_RESULT_BACKEND = environ.get("CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL")
