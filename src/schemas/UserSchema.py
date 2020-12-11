from models.User import User
from app import ma
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User