from app import db
import flask

auth = flask.Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    json = flask.request.json
    print(json)
    return json