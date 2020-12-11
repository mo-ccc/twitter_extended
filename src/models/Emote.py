from app import db

class Emote(db.Model):
    __tablename__ = "emotes"
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(15), nullable=False, unique=True)
    url = db.Column(db.String(), nullable=False)