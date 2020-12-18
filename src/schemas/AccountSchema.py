from models.Account import Account
from app import ma
from marshmallow.validate import Email, Length
class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        dump_only = ("id", "user_id")
    email = ma.Str(required=True, validate=[Email(),])
    password = ma.Str(required=True, validate=[Length(min=5),])
    