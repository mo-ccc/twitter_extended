import flask
import json
import flask_jwt_extended
from models.User import User
from models.Emote import Emote
from models.Tweet import Tweet
from app import db
import os
from PIL import Image

emotes = flask.Blueprint("emotes", __name__)

@emotes.route("/emotes", methods=["GET"])
@flask_jwt_extended.jwt_required
def get_management():
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user:
        flask.abort(400, description="something went wrong")
    
    owned_emotes = Emote.query.filter_by(author_id=user.id).all()
    
    return flask.render_template("manage_emotes.html", user=user, auth=jwt_id, owned_emotes=owned_emotes)

@emotes.route("/emotes", methods=["POST"])
@flask_jwt_extended.jwt_required
def create_emote():
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user:
        flask.abort(400, description="something went wrong")

    name = flask.request.form.get("name")
    if 'image' not in flask.request.files:
        flask.abort(400, description='No image') 

    image = flask.request.files["image"]
    file_extension = os.path.splitext(image.filename)[1]
    if file_extension not in [".jpg", ".png", ".jpeg"]:
        flask.abort(400, description="Not an image")

    pil_image = Image.open(image)
    pil_image = pil_image.resize((250,250), Image.ANTIALIAS)
        
    from werkzeug.utils import secure_filename
    secure = secure_filename(f"{name}.png")
    emote = Emote(name=name, url=f"emotes/{secure}", user=user)
    db.session.add(emote)
    db.session.commit()
    
    
    pil_image.save(f"static/emotes/{secure}")
    
    return flask.redirect('/emotes', code=302)
    
@emotes.route("/emotes/<int:id>", methods=["GET"])
@flask_jwt_extended.jwt_optional
def display_emote(id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    emote = Emote.query.filter_by(id=id).first_or_404()
    tweets = Tweet.query.filter(Tweet.emotes.any(id=emote.id)).all()
    return flask.render_template("emote_page.html", emote=emote, tweets=tweets, auth=jwt_id)
    
@emotes.route("/emotes/search/<name>", methods=["GET"])
def alternate_emote_url(name):
    emote = Emote.query.filter_by(name=name).first_or_404()
    return flask.redirect(f"/emotes/{emote.id}", code=302)
   
@emotes.route("/emotes/<int:id>", methods=["POST"])
@flask_jwt_extended.jwt_required
def favourite_emote(id):
    jwt_id = flask_jwt_extended.get_jwt_identity()
    user = User.query.get(jwt_id)
    if not user:
        flask.abort(400, description="something went wrong")
    
    is_favourited = Emote.query.filter(Emote.favouriter.any(id=user.id)).filter_by(id=id).first()
    if not is_favourited:
        user.favourites.append(Emote.query.get(id))
        flask.flash('added')
    else:
        user.favourites.remove(Emote.query.get(id))
        flask.flash('removed')
    
    db.session.commit()
    return flask.redirect(f"/emotes/{id}", code=302)
    
@emotes.route("/emotes/<int:id>", methods=["DELETE"])
@flask_jwt_extended.jwt_required
def delete_emote(id):
    jwt_id = flask_jwt_extended.get_jwt_identity
    user = User.query.get(jwt_id)
    if not user:
        flask.abort(400, description="something went wrong")
    
    emote = Emote.query.filter_by(id=id).first_or_404()
    
    if emote.author_id != user.id:
        flask.abort(400, description="you do not have permission to do that")
    
    os.remove(os.path.join('/static', emote.url))
    db.session.delete(emote)
    db.session.commit()
    return flask.redirect("/emotes", code=302)