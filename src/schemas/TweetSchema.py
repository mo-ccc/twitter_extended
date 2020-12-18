from models.Tweet import Tweet
from app import ma
from marshmallow.validate import Length
class TweetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tweet
        dump_only = (
            "id",
            "author_id",
            "created_at",
            "conversation_id",
            "possibly_sensitive"
        )
    text = ma.Str(required=True, validate=[Length(min=1, max=280),])