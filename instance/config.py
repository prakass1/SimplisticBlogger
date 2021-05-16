# Adding secret infos here
from os import environ

class Config(object):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CSRF_ENABLED = True
    CACHE_TYPE = environ.get("CACHE_TYPE")
    CACHE_DEFAULT_TIMEOUT = environ.get("CACHE_DEFAULT_TIMEOUT")
    SECRET_KEY = environ.get("SECRET_KEY")
    DB_DRIVER = environ.get("DB_DRIVER")
    DB_HOST = environ.get("DB_HOST")
    DB_PORT = environ.get("DB_PORT")
    DB_USER = environ.get("DB_USER")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DATABASE_NAME = environ.get("DB_NAME")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_DEBUG = False
    db_uri = DB_DRIVER + "://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + ":" + DB_PORT + "/" + DATABASE_NAME


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.db_uri


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.db_uri
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.db_uri
    SQLALCHEMY_ECHO = True


app_config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig
}