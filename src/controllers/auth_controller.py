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
    from services.forms import RegisterForm
    form = RegisterForm()
    return flask.render_template("register.html", form=form)

@auth.route("/register", methods=["POST"])
def register():
    data = flask.request.form.to_dict()
    account_json = {
        "email" : data["email"],
        "password" : data["password"]
    }
    user_json = {
        "name" : data["name"],
        "screen_name" : data["name"]
    }
    
    user_schema = UserSchema(partial=True)
    user_data = user_schema.load(user_json)
    new_user = User(
        name = user_data["name"],
        screen_name = user_data["screen_name"],
    )
    
    
    account_schema = AccountSchema()
    account_data = account_schema.load(account_json)
    new_account = Account(
        email = account_data["email"],
        password = bcrypt.generate_password_hash(account_data["password"]).decode('utf-8'),
        user = new_user,
    )
    
    db.session.add(new_user)
    db.session.add(new_account)
    db.session.commit()
    
    return 'ok'
    
@auth.route("/login", methods=["GET"])
def login_page():
    from services.forms import LoginForm
    form = LoginForm()
    return flask.render_template("login.html", form=form)
    
@auth.route("/login", methods=["POST"])
def login():
    data = flask.request.form.to_dict()
    
    account_data = AccountSchema().load(data)
    
    account = Account.query.filter_by(email=account_data["email"]).first()
    if not account:
        flask.abort(400, description='Invalid login')
    
    if bcrypt.check_password_hash(account.password, account_data["password"]):
        token = flask_jwt_extended.create_access_token(
            identity=account.user_id, 
            expires_delta=datetime.timedelta(days=1)
        )
        response = flask.redirect(f"/users/{account.user_id}", code=302)
        flask_jwt_extended.set_access_cookies(response, token)
        return response
    flask.abort(400, description='Invalid login')