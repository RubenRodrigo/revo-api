from bd import connection
from sqlalchemy import types, Column
from uuid import uuid4

class UserModel(connection.Model):
    id = Column(type_=types.UUID, default=uuid4, primary_key=True, unique=True)
    name = Column(type_=types.Text, nullable=True)
    email = Column(type_=types.Text, nullable=False, unique=True)
    password = Column(type_=types.Text, nullable=False)

    __tablename__='users'