from models.Tweet import Tweet
from app import ma
from marshmallow.validate import Length
class TweetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tweet
    text = ma.Str(required=True, validate=[Length(min=1, max=280),])