from app import db

class Account(db.Model):
    __tablename__ = "accounts"
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False,
        primary_key = True
    )
    
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)