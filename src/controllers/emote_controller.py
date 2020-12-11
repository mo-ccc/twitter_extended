import flask
import json
import flask_jwt_extended
from models.User import User
from models.Emote import Emote
from app import db
import os

emotes = flask.Blueprint("emotes", __name__)

@emotes.route("/emotes", methods=["POST",])
@flask_jwt_extended.jwt_required
def create_emote():
    jwt_user = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_user)
    if not user:
        flask.abort(400, description="something went wrong")

    json_data = json.loads(flask.request.form.get('json'))
    if 'image' not in flask.request.files:
        flask.abort(400, description='No emote')
        
    image = flask.request.files["image"]
    
    image.save("image.jpg")
    
    emote = Emote(name="duck", url="image.jpg", user=user)
    db.session.add(emote)
    db.session.commit()
    
    return 'ok'
    
@emotes.route("/emotes/<id>", methods=["GET",])
def display_emote(id):
    return f"<img src=\"{flask.url_for('static', filename='image.jpg')}\">"