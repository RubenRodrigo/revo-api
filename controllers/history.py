from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from bd import connection
from models import UserModel, HistoryModel
from .serializers import HistorySerializer

class HistoryController(Resource):
    serializer = HistorySerializer()

    @jwt_required()
    def get(self):
        user_identity = get_jwt_identity()

        current_user = connection.session.query(UserModel).filter(UserModel.id == user_identity).first()
        histories = connection.session.query(HistoryModel).filter(HistoryModel.userId == current_user.id).order_by(HistoryModel.createdAt.desc()).all()
        data = self.serializer.dump(histories,many=True)

        return {
            'content': data
        }