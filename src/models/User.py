from app import db
from models.Account import Account
from models.Tweet import Tweet
from models.Emote import Emote
from models.Favourite_Emotes import favourite_emotes

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    screen_name = db.Column(db.String(20), nullable=False)
    
    account = db.relationship('Account', backref='user', uselist=False)
    tweets = db.relationship('Tweet', backref='user')
    emotes = db.relationship('Emote', backref='user')
    favourites = db.relationship(
        'Emote',
        secondary='favourite_emotes',
        backref='favouriter')