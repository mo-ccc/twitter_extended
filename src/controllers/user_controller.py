import flask
from models.User import User
from models.Tweet import Tweet
from schemas.UserSchema import UserSchema
from schemas.TweetSchema import TweetSchema

users = flask.Blueprint("users", __name__)

@users.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    user_dump = UserSchema().dump(user)
    
    tweets = Tweet.query.filter_by(author_id=id).all()
    tweets_dump = TweetSchema(many=True).dump(tweets)
    
    return flask.jsonify({"author": user_dump, "tweets": tweets_dump})