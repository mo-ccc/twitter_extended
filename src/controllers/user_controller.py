import flask
from models.User import User
from models.Tweet import Tweet
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
    
    logged_in_user = flask_jwt_extended.get_jwt_identity()
    if logged_in_user == user.id:
        return flask.render_template("user_page.html", tweets=tweets_dump, user=user_dump, auth=True)
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
    
    db.session.add(tweet)
    db.session.commit()
    return flask.redirect(f"/users/{id}", code=302)
    