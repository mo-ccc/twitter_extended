import flask
import flask_jwt_extended
from app import db
from schemas.TweetSchema import TweetSchema
from models.Tweet import Tweet
from models.User import User
from models.Emote import Emote

tweets = flask.Blueprint('tweets', __name__)

@tweets.route("/", methods=["GET"])
@flask_jwt_extended.jwt_optional
def homepage():
    jwt_id = flask_jwt_extended.get_jwt_identity()

    tweets = Tweet.query.order_by(Tweet.id.desc()).all()

    return flask.render_template("homepage.html", tweets=tweets, auth=jwt_id)
    
@tweets.route('/tweet', methods=['POST'])
@flask_jwt_extended.jwt_required
def send_tweet():
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
    return flask.redirect(f"/users/{jwt_id}", code=302)
    
def parse_emotes(text):
  result = []
  splited = text.split(":")
  for x in splited:
    if " " not in x and x and x not in result:
      result.append(x)
  return result
  
@tweets.route('/tweet/<int:id>',methods=['DELETE'])
@flask_jwt_extended.jwt_required
def delete_tweet():
    tweet = Tweet.query.filter_by(id=id).first_or_404()

    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    
    if not user or user.id != tweet.author_id and not user.is_admin:
        flask.abort(400, description="Invalid request")
    
    db.session.delete(tweet)
    db.session.commit()
    return flask.redirect(f"/users/{jwt_id}", code=302)