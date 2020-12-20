from app import db
import flask
from schemas.UserSchema import UserSchema
from schemas.AccountSchema import AccountSchema
from models.User import User
from models.Account import Account
from app import db, bcrypt
import flask_jwt_extended
import datetime

auth = flask.Blueprint("auth", __name__)

@auth.route("/register", methods=["GET"])
def register_page():
    return flask.render_template("register.html")

@auth.route("/register", methods=["POST"])
def register():
    data = flask.request.form.to_dict()
    # separating items from the request
    account_dict = {
        "email" : data["email"],
        "password" : data["password"]
    }
    user_dict = {
        "name" : data["name"],
        "screen_name" : data["name"]
    }
    
    user_schema = UserSchema(partial=True)
    user_data = user_schema.load(user_dict)
    new_user = User(
        name = user_data["name"],
        screen_name = user_data["screen_name"],
    )
    
    account_schema = AccountSchema()
    account_data = account_schema.load(account_dict)
    new_account = Account(
        email = account_data["email"],
        password = bcrypt.generate_password_hash(account_data["password"]).decode('utf-8'),
        user = new_user,
    )
    
    # in the case where the email or name already exists this is needed
    from sqlalchemy.exc import IntegrityError
    from psycopg2.errors import UniqueViolation
    try:
        db.session.add(new_user)
        db.session.add(new_account)
        db.session.commit()
        
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            # will let the person trying to register know
            return flask.abort(400, description='email or name already exists')
        
    flask.flash("registration successful")
    
    return flask.redirect('/', code=302)
    
@auth.route("/login", methods=["GET"])
def login_page():
    return flask.render_template("login.html")
    
@auth.route("/logout", methods=["GET"])
def logout():
    flask.flash("logout successful")
    response = flask.redirect("/", code=302)
    response.delete_cookie(key='access_token_cookie', path='/')
    return response
    
@auth.route("/login", methods=["POST"])
def login():
    data = flask.request.form.to_dict()
    
    # if a validaion error occurs present invalid login screen
    from marshmallow.exceptions import ValidationError
    try:
        account_data = AccountSchema().load(data)
    except ValidationError as e:
        flask.abort(400, description='Invalid login')
    
    account = Account.query.filter_by(email=account_data["email"]).first()
    if not account:
        flask.abort(400, description='Invalid login')
    
    if not bcrypt.check_password_hash(account.password, account_data["password"]):
        flask.abort(400, description='Invalid login')
        
    token = flask_jwt_extended.create_access_token(
            identity=account.user_id, 
            expires_delta=datetime.timedelta(days=1)
        )
    flask.flash("login successful")
    response = flask.redirect(f"/users/{account.user_id}", code=302)
    # set the access cookies
    flask_jwt_extended.set_access_cookies(response, token)
    return response