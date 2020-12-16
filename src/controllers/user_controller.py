import flask
from models.User import User
from models.Tweet import Tweet
from models.Emote import Emote
from models.Favourite_Emotes import favourite_emotes
from schemas.UserSchema import UserSchema
from schemas.TweetSchema import TweetSchema
import flask_jwt_extended
from app import db

users = flask.Blueprint("users", __name__)

@users.route('/users/<id>', methods=['GET'])
@flask_jwt_extended.jwt_optional
def get_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    
    tweets = Tweet.query.filter_by(author_id=id).order_by(Tweet.id.desc()).all()
    
    favourites = Emote.query.filter(Emote.favouriter.any(id=id)).all()
    
    jwt_id = flask_jwt_extended.get_jwt_identity()
    if jwt_id == user.id:
        return flask.render_template("user_page.html", tweets=tweets, user=user, auth=jwt_id, favourite_emotes=favourites)
    return flask.render_template("user_page.html", tweets=tweets, user=user)
    

    