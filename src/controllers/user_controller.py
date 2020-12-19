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

@users.route('/users/<int:id>', methods=['GET'])
@flask_jwt_extended.jwt_optional
def get_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    
    tweets = Tweet.query.filter_by(author_id=id).order_by(Tweet.id.desc()).all()
    
    favourites = Emote.query.filter(Emote.favouriter.any(id=id)).all()
    
    jwt_id = flask_jwt_extended.get_jwt_identity()
    if jwt_id == user.id:
        return flask.render_template("user_page.html", tweets=tweets, user=user, auth=jwt_id, favourite_emotes=favourites, owner=True)
        
    
    owned_emotes = Emote.query.filter_by(author_id=id).all()
    
    return flask.render_template("user_page.html", tweets=tweets, user=user, owned_emotes=owned_emotes, auth=jwt_id)

@users.route('/users/<int:id>', methods=['PUT'])
@flask_jwt_extended.jwt_required
def update_user(id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(id)
    if not user or jwt_id != user.id and not user.is_admin:
        flask.abort(400, description="Not allowed")
    
    data = flask.request.form.to_dict()
    
    user_schema = UserSchema(partial=True, exclude=('name',))
    
    try:
        valid_data = user_schema.load(data, exclude=("verified",))
    except:
        flask.abort(400, description="Invalid request")
    
    for v in valid_data:
        setattr(user, v, valid_data[v])
    db.session.commit()
    flask.flash("updated user")
    return 'ok'

@users.route('/users/<int:id>', methods=['DELETE'])
@flask_jwt_extended.jwt_required
def delete(id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(id)
    
    if not user or jwt_id != user.id and not user.is_admin:
        flask.abort(400, description="Not allowed")
    
    db.session.delete(user)
    db.session.commit()
    return 'ok'
    
@users.route('/settings', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_settings():
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    
    if not user:
        flask.abort(400, description="Not allowed")
        
    return flask.render_template('settings.html')