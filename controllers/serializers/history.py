from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import HistoryModel

class HistorySerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = HistoryModel