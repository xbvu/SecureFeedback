import os

from SecureWebApp.utils import INSTANCE_FOLDER_PATH


class BaseConfig(object):
    PROJECT = "SecureWebApp"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DEBUG = False
    SECRET_KEY = 'secret key'
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')


class DefaultConfig(BaseConfig):
    DEBUG = False

    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + INSTANCE_FOLDER_PATH + '/sources.sqlite'