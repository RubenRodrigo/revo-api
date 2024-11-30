from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models import UserModel
from marshmallow import Schema, fields

class UserRegisterSerializer(SQLAlchemyAutoSchema):
    password = auto_field(load_only=True)

    class Meta:
        model = UserModel

class UserLoginSerializer(Schema):
    password = fields.Str(required=True)
    email = fields.Email(required=True)