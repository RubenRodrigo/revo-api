from flask_restful import Resource, request
from .serializers import RecommendationSerializer
from flask_jwt_extended import jwt_required, get_jwt_identity
from recommender import recommend
from models import HistoryModel
from bd import connection

class RecommendationController(Resource):
    serializer = RecommendationSerializer()
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        validated_data = self.serializer.load(data)
        user_identity = get_jwt_identity()

        if validated_data.get('primaryTechStack') not in validated_data.get('techStacks'):
            return {
                'message': 'The primary tech stack should be in the tech stacks list'
            }, 400
        
        
        # TODO: Add the recommended system here to get the result and retrieve to the frontend
        result = recommend({
            "seniorityLevel":validated_data.get("seniority"),
            "englishLevel":validated_data.get("english"),
            "techStack":validated_data.get("techStacks"),
            "primaryTechStack": validated_data.get("primaryTechStack"),
            "hoursPerWeek": validated_data.get("hoursPerWeek"),
            "teamLead": validated_data.get("teamLead"),
            "flexibleSchedule": validated_data.get("flexibleSchedule"),
            "days": validated_data.get("days"),
        })

        new_history = HistoryModel(**validated_data, result=result, userId=user_identity)
        
        connection.session.add(new_history)
        connection.session.commit()
        
        return {
            'content': result
        }, 200