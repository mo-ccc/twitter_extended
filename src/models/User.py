from app import db
from models.Account import Account
from models.Tweet import Tweet
from models.Emote import Emote
from models.Favourite_Emotes import favourite_emotes
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    
    screen_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=False),
        nullable=False,
        default=datetime.utcnow
    )

    verified = db.Column(db.Boolean(), default=False)
    is_default = db.Column(db.Boolean(), default=True)
    is_admin = db.Column(db.Boolean(), default=False)
    
    # backref means account has a reference to user i.e. account.user
    account = db.relationship('Account', backref='user', uselist=False, passive_deletes='all')
    tweets = db.relationship('Tweet', backref='user', passive_deletes='all')
    emotes = db.relationship('Emote', backref='user')
    favourites = db.relationship(
        'Emote',
        secondary='favourite_emotes',
        backref='favouriter',
        passive_deletes='all'
    )