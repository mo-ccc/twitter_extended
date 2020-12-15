from app import db
from models.Emote import Emote
from models.Tweet_Emote_Joint import tweet_emote_joint
import enum
from datetime import datetime

class FilterLevel(enum.Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2


class Tweet(db.Model):
    __tablename__ = "tweets"
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
        default=datetime.utcnow)
    
    source_device = db.Column(db.String())
    in_reply_to_tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    possibly_sensitive = db.Column(db.Boolean())
    filter_level = db.Column(db.Enum(FilterLevel))
    
    emotes = db.relationship(
        'Emote',
        secondary='tweet_emote_joint',
        backref='tweet'
    )
    


    