from enum import Enum
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import os

class EnglishLevel(Enum):
    ADVANCED = '3'
    PROFICIENT = '2'
    BASIC = '1'

class Seniority(Enum):
    SENIOR = '6'
    MID_SENIOR = '5'
    MID = '4'
    JUNIOR_MID = '3'
    JUNIOR = '2'
    TRAINEE = '1'


class TalentRecommender:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.prepare_data()
        self.fit_model()

    def prepare_data(self):
        # Get tech stack columns (excluding non-tech columns)
        basic_cols = ['id', 'name', 'weekly_available_hours', 'seniority_level', 
                     'english_level', 'number_of_assignments', 'active_assignments', 
                     'assignment_avg', 'tag_names']
        self.tech_cols = [col for col in self.df.columns if col not in basic_cols]
        
        # Prepare feature matrix
        feature_cols = ['weekly_available_hours', 'seniority_level', 'english_level', 
                       'assignment_avg'] + self.tech_cols
        self.X = self.df[feature_cols].copy()
        
        # Scale numerical features
        self.scaler = StandardScaler()
        numerical_cols = ['weekly_available_hours', 'assignment_avg']
        self.X[numerical_cols] = self.scaler.fit_transform(self.X[numerical_cols])

    def fit_model(self):
        self.model = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.model.fit(self.X)

    def map_seniority(self, seniority_str):
        try:
            return Seniority[seniority_str.upper()].value
        except (KeyError, AttributeError):
            return Seniority.MID.value

    def invert_map_seniority(self, seniority_val):
        try:
            return Seniority[seniority_val].name
        except (KeyError, AttributeError):
            return Seniority.MID.name

    def map_english(self, english_str):
        try:
            return EnglishLevel[english_str.upper()].value
        except (KeyError, AttributeError):
            return EnglishLevel.PROFICIENT.value

    def create_input_vector(self, request_data):
        # Initialize input vector with zeros
        input_vector = pd.DataFrame(0, index=[0], columns=self.X.columns)
        
        # Fill basic features
        input_vector['weekly_available_hours'] = request_data.get('hoursPerWeek', 0)
        input_vector['seniority_level'] = self.map_seniority(request_data.get('seniorityLevel', 'MID'))
        input_vector['english_level'] = self.map_english(request_data.get('englishLevel', 'PROFICIENT'))
        input_vector['assignment_avg'] = 0  # Default value
        
        # Fill tech stack
        tech_stack = request_data.get('techStack', [])
        primary_tech = request_data.get('primaryTechStack')
        
        for tech in tech_stack:
            if tech in self.tech_cols:
                seniority_value = self.map_seniority(request_data.get('seniorityLevel', 'MID'))
                # Give higher weight to primary tech stack
                if tech == primary_tech:
                    input_vector[tech] = seniority_value  # Use the actual seniority level for primary tech
                else:
                    input_vector[tech] = 0# One level lower for secondary skills
        
        # Scale numerical features
        numerical_cols = ['weekly_available_hours', 'assignment_avg']
        input_vector[numerical_cols] = self.scaler.transform(input_vector[numerical_cols])
        
        return input_vector

    def get_recommendations(self, request_data, n_recommendations=5):
        input_vector = self.create_input_vector(request_data)
        
        # Find nearest neighbors
        distances, indices = self.model.kneighbors(input_vector)
        
        # Get recommended profiles
        recommendations = []
        for idx, distance in zip(indices[0], distances[0]):
            profile = self.df.iloc[idx]
            tech_skills = {tech: self.invert_map_seniority(int(profile[tech])) for tech in self.tech_cols if profile[tech] > 0}
            
            recommendations.append({
                'id': profile['id'],
                'name': profile['name'],
                'similarity_score': round(float(1 / (1 + distance)), 3),
                'weekly_available_hours': int(profile['weekly_available_hours']),
                'seniority_level': self.invert_map_seniority(int(profile['seniority_level'])),
                'english_level': int(profile['english_level']),
                'tech_skills': tech_skills,
                'assignment_avg': int(profile['assignment_avg']),
                'active_assignments': int(profile['active_assignments'])
            })
        
        # Sort by similarity score in descending order
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return recommendations

# Initialize recommender
csv_path = os.path.join('output', 'consolidated_team_data.csv')
recommender = TalentRecommender(csv_path)


def recommend(data):
    if not data:
        raise ValueError("No input data provided")
        
    required_fields = ['seniorityLevel', 'englishLevel', 'techStack']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
    recommendations = recommender.get_recommendations(data)
    
    return recommendations
   
