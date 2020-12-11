from app import db
from models.Account import Account

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    screen_name = db.Column(db.String(20), nullable=False)
    
    account = db.relationship('Account', backref='user', uselist=False)