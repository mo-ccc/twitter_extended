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
    
@users.route('/users/<id>', methods=['POST'])
@flask_jwt_extended.jwt_required
def send_tweet(id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user:
        flask.abort(400, description="something went wrong")
    
    data = flask.request.form.to_dict()
    tweet_data = TweetSchema().load(data, partial=("author_id"))
    input_content = tweet_data["text"] + " "
    tweet = Tweet(text=input_content, user=user)
    
    # filter out emotes from the tweet and add tweet+emotes to the tweet_emote_joint table
    emotes_in_tweet = parse_emotes(tweet_data["text"])
    emotes = [Emote.query.filter_by(name=x).first() for x in emotes_in_tweet]
    for x in emotes:
        if x:
            tweet.emotes.append(x)
    
    db.session.add(tweet)
    db.session.commit()
    return flask.redirect(f"/users/{id}", code=302)
    
def parse_emotes(text):
  result = []
  splited = text.split(":")
  for x in splited:
    if " " not in x and x and x not in result:
      result.append(x)
  return result
    