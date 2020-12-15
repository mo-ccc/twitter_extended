from app import db

tweet_emote_joint = db.Table(
    'tweet_emote_joint',
    db.Column('tweet_id', db.Integer, db.ForeignKey('tweets.id'), primary_key=True),
    db.Column('emote_id', db.Integer, db.ForeignKey('emotes.id'), primary_key=True)
)