from models.User import User
from app import ma
from marshmallow.validate import Length
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        dump_only = ("id", "created_at", "is_admin", "is_default")
    name = ma.Str(required=True, validate=[Length(min=1),])
    screen_name = ma.Str(required=True, validate=[Length(min=1),])