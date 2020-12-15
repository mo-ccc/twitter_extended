import flask
import flask_jwt_extended
from app import db
from schemas.TweetSchema import TweetSchema
from models.Tweet import Tweet
from models.User import User

tweets = flask.Blueprint('tweets', __name__)

@tweets.route("/", methods=["GET"])
@flask_jwt_extended.jwt_optional
def homepage():
    jwt_id = flask_jwt_extended.get_jwt_identity()

    tweets = Tweet.query.order_by(Tweet.id.desc()).all()
    
    return flask.render_template("homepage.html", tweets=tweets, auth=jwt_id)
    

