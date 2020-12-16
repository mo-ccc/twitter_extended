from models.User import User
from app import ma
from marshmallow.validate import Length
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    name = ma.Str(required=True, validate=[Length(min=1),])
    screen_name = ma.Str(required=True, validate=[Length(min=1),])