from flask import Flask, request
from bd import connection
from models import *
from os import environ
from dotenv import load_dotenv
from flask_restful import Api
from controllers import *
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config["JWT_SECRET_KEY"] = environ.get('JWT_SECRET')
app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(hours=1)


api = Api(app)
JWTManager(app)
connection.init_app(app)

Migrate(app,db=connection)

@app.errorhandler(IntegrityError)
def handleIntegrityError(error):
    return {
        'message':'The current user already exists'
    }, 400

@app.errorhandler(ValidationError)
def handleValidationError(error):
    return {
        'message': 'Error when validating the data',
        'content': error.args
    }, 400

api.add_resource(RecommendationController, '/recommendation')
api.add_resource(RegisterController, '/register')
api.add_resource(LoginController, '/login')
api.add_resource(HistoryController, '/history')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)