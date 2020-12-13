import flask
import flask_jwt_extended
from app import db
from schemas.TweetSchema import TweetSchema
from models.Tweet import Tweet
from models.User import User

tweets = flask.Blueprint('tweets', __name__)

