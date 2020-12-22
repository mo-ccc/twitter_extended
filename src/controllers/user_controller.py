import flask
from models.User import User
from models.Tweet import Tweet
from models.Emote import Emote
from models.Account import Account
from models.Favourite_Emotes import favourite_emotes
from schemas.UserSchema import UserSchema
from schemas.TweetSchema import TweetSchema
from schemas.AccountSchema import AccountSchema
import flask_jwt_extended
from app import db, bcrypt

users = flask.Blueprint("users", __name__)

@users.route('/users/<int:id>', methods=['GET'])
@flask_jwt_extended.jwt_optional
def get_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    
    # returns all tweets the user made ordered by id
    tweets = Tweet.query.filter_by(author_id=id).order_by(Tweet.id.desc()).all()
    
    # returns all the emotes the user has favourited
    favourites = Emote.query.filter(Emote.favouriter.any(id=id)).all()
    
    # if logged in as the user display page with the ability to make tweets
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
    
    user_schema = UserSchema(partial=True, exclude=('name',"verified"))
    
    try:
        valid_data = user_schema.load(data)
    except Exception as e:
        print(e)
        flask.abort(400, description="Invalid request")
    
    # for all parts of the request update the user with the info provided
    for v in valid_data:
        setattr(user, v, valid_data[v])
    db.session.commit()
    flask.flash("updated user")
    # return must not be a redirect to prevent infinite loop
    return 'ok'
    
@users.route('/users/<int:id>', methods=['PATCH'])
@flask_jwt_extended.jwt_required
def update_user_security(id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    account = Account.query.get(id)
    if not account or jwt_id != account.user_id:
        flask.abort(400, description="Not allowed")
    
    data = flask.request.form.to_dict()
    
    # in the request a confimation pass is sent to prevent hackers from changing pass
    confirm_pass = data.pop('confirm')
    # check if the pass matches
    if not bcrypt.check_password_hash(account.password, confirm_pass):
        flask.abort(400, description="Invalid password")
    
    account_schema = AccountSchema(partial=True)
    try:
        valid_data = account_schema.load(data)
    except Exception as e:
        print(e)
        flask.abort(400, description="Invalid request")
    
    # if user is updating password hash it
    if 'password' in valid_data:
        valid_data["password"] = bcrypt.generate_password_hash(valid_data["password"]).decode('utf-8')
    
    # for all parts of the request update the account with the info provided
    for v in valid_data:
        setattr(account, v, valid_data[v])
    db.session.commit()
    flask.flash("updated user")
    return 'ok'

@users.route('/users/<int:id>', methods=['DELETE'])
@flask_jwt_extended.jwt_required
def delete(id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(id)
    account = Account.query.get(id)
    
    if not user or jwt_id != user.id and not user.is_admin:
        flask.abort(400, description="Not allowed")
    
    body = flask.request.form.to_dict()
    password = body["confirm"]
    if not password or not bcrypt.check_password_hash(account.password, password):
        flask.abort(400, description="invalid password")
    
    db.session.delete(user)
    db.session.commit()
    flask.flash('deleted')
    return 'ok'
    
@users.route('/settings', methods=['GET'])
@flask_jwt_extended.jwt_required
def get_settings():
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user:
        flask.abort(400, description="Not allowed")
        
    # returns setting page for user where they can update their details
    return flask.render_template('settings.html', user=user, auth=jwt_id)