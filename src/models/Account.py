from main import db

class Account(db.Model):
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)