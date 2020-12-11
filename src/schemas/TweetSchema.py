from models.Tweet import Tweet
from app import ma
class TweetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tweet