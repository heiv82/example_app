import os


class Configuration(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sajdKWD&^*&@^#@6768726873WQT*T2'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:<password>@db/db_dates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_URL_BASE = "http://chirpstack-application-server:8080/"

    ROWS_PER_PAGE = 14

