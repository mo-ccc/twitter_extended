import flask_sqlalchemy
import psycopg2

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = 'secret'