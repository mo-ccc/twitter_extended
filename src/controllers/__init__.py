import flask
from controllers.user_controller import users
from controllers.auth_controller import auth
from controllers.tweet_controller import tweets

blueprints = [users, auth, tweets]