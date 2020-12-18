from app import db

tweet_emote_joint = db.Table(
    'tweet_emote_joint',
    db.Column(
        'tweet_id',
        db.Integer, 
        db.ForeignKey('tweets.id', ondelete='CASCADE'), 
        primary_key=True
    ),
    
    db.Column(
        'emote_id',
        db.Integer, 
        db.ForeignKey('emotes.id', ondelete='CASCADE'), 
        primary_key=True
    )
)