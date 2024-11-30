from flask_restful import Resource, request
from bd import connection
from .serializers import UserRegisterSerializer, UserLoginSerializer
from models import UserModel
from bcrypt import gensalt, hashpw, checkpw
from flask_jwt_extended import create_access_token

class RegisterController(Resource):
    serializer = UserRegisterSerializer()

    def post(self):
        data = request.get_json()
        validated_data: dict[str: str] = self.serializer.load(data)

        new_user = UserModel(**validated_data)
        salt = gensalt()
        password = hashpw(validated_data.get('password').encode('utf-8'), salt).decode('utf-8')
        new_user.password = password

        connection.session.add(new_user)
        connection.session.commit()
        result = self.serializer.dump(new_user)
        token = create_access_token(new_user.id)
        result['token'] = token

        return {
            'message':'User created successfully',
            'content': result
        }, 201
        
      
class LoginController(Resource):
    serializer = UserLoginSerializer()

    def post(self):
        data = request.get_json()
        validated_data: dict[str: str] = self.serializer.load(data)

        user = connection.session.query(UserModel).filter(UserModel.email == validated_data.get('email')).first()
 
        if not user:
            return {
                'message': 'User not found'
            }, 404
        password_validated = checkpw(validated_data.get('password').encode('utf-8'),user.password.encode('utf-8'))

        user_serializer = UserRegisterSerializer()
        user_data = user_serializer.dump(user)
        if password_validated:
            token = create_access_token(user.id)
            result = user_data
            result['token'] = token

            return result

        else:
            return {
                'message': 'Invalid credentials'
            }, 403
        