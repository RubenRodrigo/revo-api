from marshmallow import fields, Schema

class RecommendationSerializer(Schema):
    seniority = fields.Str(required=True)
    english = fields.Str(required=True)
    techStacks = fields.List(fields.Str())
    primaryTechStack = fields.Str(required=True)
    hoursPerWeek = fields.Int(required=True)
    teamLead = fields.Bool()
    flexibleSchedule = fields.Bool()