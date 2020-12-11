from app import db
import flask
from schemas.UserSchema import UserSchema
from schemas.AccountSchema import AccountSchema
from models.User import User
from models.Account import Account

auth = flask.Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = flask.request.json
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
        screen_name = user_data["screen_name"]
    )
    
    
    account_schema = AccountSchema()
    account_data = account_schema.load(account_json)
    new_account = Account(
        email = account_data["email"],
        password = account_data["password"],
        user = new_user
    )
    
    db.session.add(new_user)
    db.session.add(new_account)
    db.session.commit()
    
    return account_schema.dump(Account.query.get(1))