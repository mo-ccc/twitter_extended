from app import db


class Tweet(db.Model):
    __tablename__ = "tweets"
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(280), nullable=False)
    