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
    user_dump = UserSchema().dump(user)
    
    tweets = Tweet.query.filter_by(author_id=id).order_by(Tweet.id.desc()).all()
    tweets_dump = TweetSchema(many=True).dump(tweets)
    
    favourites = Emote.query.filter(Emote.favouriter.any(id=id)).all()
    
    logged_in_user = flask_jwt_extended.get_jwt_identity()
    if logged_in_user == user.id:
        return flask.render_template("user_page.html", tweets=tweets_dump, user=user_dump, auth=True, favourite_emotes=favourites)
    return flask.render_template("user_page.html", tweets=tweets_dump, user=user_dump)
    
@users.route('/users/<id>', methods=['POST'])
@flask_jwt_extended.jwt_required
def send_tweet(id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user:
        flask.abort(400, description="something went wrong")
    
    data = flask.request.form.to_dict()
    tweet_data = TweetSchema().load(data, partial=("author_id"))
    tweet = Tweet(text=tweet_data["text"], user=user)
    
    emotes_in_tweet = parse_emotes(tweet_data["text"])
    emotes = [Emote.query.filter_by(name=x).first() for x in emotes_in_tweet]
    for x in emotes:
        tweet.emotes.append(x)
    
    db.session.add(tweet)
    db.session.commit()
    return flask.redirect(f"/users/{id}", code=302)
    
def parse_emotes(text):
  result = []
  splited = text.split(":")
  for x in splited:
    if " " not in x and x:
      result.append(x)
  return result
    