from app import db
from models.Emote import Emote
from models.Tweet_Emote_Joint import tweet_emote_joint


class Tweet(db.Model):
    __tablename__ = "tweets"
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(280), nullable=False)
    
    emotes = db.relationship(
        'Emote',
        secondary='tweet_emote_joint',
        backref='tweet'
    )
    