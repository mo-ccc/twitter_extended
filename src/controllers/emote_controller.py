import flask
import json
import flask_jwt_extended
from models.User import User
from models.Emote import Emote
from app import db
import os
from PIL import Image

emotes = flask.Blueprint("emotes", __name__)

@emotes.route("/emotes", methods=["POST",])
@flask_jwt_extended.jwt_required
def create_emote():
    jwt_user = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_user)
    if not user:
        flask.abort(400, description="something went wrong")

    json_data = json.loads(flask.request.form.get('json'))
    name = json_data["name"]
    if 'image' not in flask.request.files:
        flask.abort(400, description='No image') 

    image = flask.request.files["image"]
    file_extension = os.path.splitext(image.filename)[1]
    if file_extension not in [".jpg", ".png", ".jpeg"]:
        flask.abort(400, description="Not an image")
    pil_image = Image.open(image)
    pil_image.resize((250,250), Image.ANTIALIAS)
        
    from werkzeug.utils import secure_filename
    secure = secure_filename(f"{name}.png")
    emote = Emote(name=name, url=f"static/{secure}", user=user)
    db.session.add(emote)
    db.session.commit()
    
    
    pil_image.save(f"static/{secure}")
    
    return 'ok'
    
@emotes.route("/emotes/<id>", methods=["GET",])
def display_emote(id):
    return f"<img src=\"{flask.url_for('static', filename='emote/image.jpg')}\">"