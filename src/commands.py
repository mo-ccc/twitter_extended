import flask
from app import db, bcrypt

client = flask.Blueprint('client', __name__)
    
@client.cli.command('drop')
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("dropped all tables")
    
@client.cli.command('create_admin')
def create_admin():
    email = input("email: ")
    password = input("password: ")
    name = input("name: ")
    
    user_json = {"name": name}
    account_json = {"email": email, "password": password}
    
    from schemas.UserSchema import UserSchema
    user_schema = UserSchema(partial=True)
    user_data = user_schema.load(user_json)
    
    from models.User import User
    new_user = User(
        name = user_data["name"],
        screen_name = user_data["name"],
        is_admin = True
    )
    
    from schemas.AccountSchema import AccountSchema
    account_schema = AccountSchema()
    account_data = account_schema.load(account_json)

    from models.Account import Account
    new_account = Account(
        email = account_data["email"],
        password = bcrypt.generate_password_hash(account_data["password"]).decode('utf-8'),
        user = new_user
    )
    
    db.session.add(new_user)
    db.session.add(new_account)
    db.session.commit()
    