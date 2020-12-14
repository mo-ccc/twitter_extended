from app import db

favourite_emotes = db.Table(
    'favourite_emotes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('emote_id', db.Integer, db.ForeignKey('emotes.id'), primary_key=True)
)