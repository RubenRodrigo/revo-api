from bd import connection
from sqlalchemy import types, Column, ForeignKey
from sqlalchemy.sql import func
from uuid import uuid4

class HistoryModel(connection.Model):
    id = Column(type_=types.UUID, default=uuid4, primary_key=True, unique=True)
    createdAt = Column(name='created_at', type_=types.TIMESTAMP, server_default=func.now())
    seniority = Column(type_=types.Text, nullable=False)
    englishLevel = Column(type_=types.Text, nullable=False, name='english_level')
    techStacks = Column(type_=types.ARRAY(types.Text), nullable=False, name='tech_stacks')
    primaryTechStack = Column(type_=types.Text, nullable=False, name='primary_tech_stack')
    hoursPerWeek = Column(type_=types.Integer, nullable=False, name='hours_per_week')
    teamLead = Column(type_=types.Boolean, default=False, name='team_lead')
    flexibleSchedule = Column(type_=types.Boolean, default=False, name='flexible_schedule')
    result = Column(type_=types.JSON, nullable=True)

    userId = Column(ForeignKey(column='users.id'), type_=types.UUID, nullable=False, name='user_id')

    __tablename__='histories'