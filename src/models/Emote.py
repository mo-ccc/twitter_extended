from app import db
from models.Favourite_Emotes import favourite_emotes
from datetime import datetime

class Emote(db.Model):
    __tablename__ = "emotes"
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(15), nullable=False, unique=True)
    url = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)