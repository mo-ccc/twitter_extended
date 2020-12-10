import flask
from models.User import User

users = flask.Blueprint("users", __name__)

@users.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    print(users)
    for x in users:
        print(x.name)
    return 'ok'