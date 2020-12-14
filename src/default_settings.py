import flask_sqlalchemy
import psycopg2

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'secret'
SECRET_KEY = 'flashem'
MAX_CONTENT_LENGTH = 8 * 1024 * 1024
JWT_TOKEN_LOCATION = ['cookies']
JWT_COOKIE_CSRF_PROTECT = False