import flask
from controllers.user_controller import users
from controllers.auth_controller import auth

blueprints = [users, auth]