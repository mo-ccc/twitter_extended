import flask
from controllers.user_controller import users
from controllers.auth_controller import auth
from controllers.tweet_controller import tweets
from controllers.emote_controller import emotes
from controllers.admin_controller import admins

blueprints = [users, auth, tweets, emotes, admins]