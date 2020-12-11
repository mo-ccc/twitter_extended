import flask
import flask_jwt_extended
from app import db
from schemas.TweetSchema import TweetSchema
from models.Tweet import Tweet
from models.User import User

tweets = flask.Blueprint('tweets', __name__)

@tweets.route('/tweet', methods=['POST'])
@flask_jwt_extended.jwt_required
def create_tweet():
    jwt_user = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_user)
    if not user:
        flask.abort(400, description="something went wrong")
    
    data = flask.request.json
    tweet_data = TweetSchema().load(data, partial=("author_id"))
    tweet = Tweet(text=tweet_data["text"], user=user)
    
    db.session.add(tweet)
    db.session.commit()
    
    return 'ok'

