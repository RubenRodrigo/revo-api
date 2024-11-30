from flask_restful import Resource, request
from .serializers import RecommendationSerializer
from recommender import recommend
class RecommendationController(Resource):
    serializer = RecommendationSerializer()
    
    def post(self):
        data = request.get_json()
        validated_data = self.serializer.load(data)
        print(validated_data)
        # TODO: Add the recommended system here to get the result and retrieve to the frontend
        result = recommend({
            "seniorityLevel":validated_data.get("seniority"),
            "englishLevel":validated_data.get("english"),
            "techStack":validated_data.get("techStacks"),
            "primaryTechStack": validated_data.get("primaryTechStack"),
            "hoursPerWeek": validated_data.get("hoursPerWeek"),
            "teamLead": validated_data.get("teamLead"),
            "flexibleSchedule": validated_data.get("flexibleSchedule")
        })
        return {
            'message': result
        }, 200