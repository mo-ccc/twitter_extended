from models.Account import Account
from app import ma
class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account