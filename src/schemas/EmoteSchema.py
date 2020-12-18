from models.Emote import Emote
from app import ma
from marshmallow.validate import Length
class EmoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Emote
        dump_only = ("id", "author_id", "url", "created_at")
    name = ma.Str(required=True, validate=Length(min=3, max=15))