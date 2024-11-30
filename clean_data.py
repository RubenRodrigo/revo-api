import pandas as pd
import json
from datetime import datetime
import os
import random
from enum import Enum
import numpy as np

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

def get_english_value(english_str):
    """
    Convert english level string to numeric value.
    Returns '0' if english level is not found.
    """
    try:
        return EnglishLevel[english_str].value
    except (KeyError, TypeError):
        return '0'

def get_seniority_value(seniority_str):
    """
    Convert seniority string to numeric value.
    Returns '0' if seniority is not found.
    """
    try:
        return Seniority[seniority_str].value
    except (KeyError, TypeError):
        return '0'


def load_and_clean_csv(filename, columns=None):
    """
    Load CSV file with specified columns
    """
    file_path = os.path.join('mb-data', filename)
    if columns:
        df = pd.read_csv(file_path, usecols=columns)
    else:
        df = pd.read_csv(file_path)
    return df

def get_random_hourly_cost():
    """
    Generate random hourly cost between 20 and 150
    """
    return round(random.uniform(20, 150), 2)

def get_assignments_with_tags(assignments_df, assignments_tags_df, tags_df):
    """
    Create a dictionary of assignments with their associated tags
    """
    tags_info = assignments_tags_df.merge(
        tags_df,
        left_on='tag_id',
        right_on='id'
    )
    
    assignment_tags = tags_info.groupby('assignment_id').apply(
        lambda x: x[['id', 'name', 'is_primary']].to_dict('records')
    ).to_dict()
    
    assignments_dict = {}
    for _, assignment in assignments_df.iterrows():
        assignment_id = assignment['id']
        
        # Handle NaN values and generate random data where needed
        notes = assignment['notes'] if pd.notnull(assignment['notes']) else ""
        seniorities = assignment['seniorities'] if pd.notnull(assignment['seniorities']) else random.choice(list(Seniority)).value
        status = assignment['status'] if pd.notnull(assignment['status']) else "active"
        hourly_cost = assignment['hourly_cost'] if pd.notnull(assignment['hourly_cost']) else get_random_hourly_cost()
        
        assignment_data = {
            'client_id': assignment['client_id'],
            'is_team_leader': bool(assignment['is_team_leader']),
            'is_flexible': bool(assignment['is_flexible']),
            'billable': bool(assignment['billable']),
            'hourly_rate': float(assignment['hourly_rate']) if pd.notnull(assignment['hourly_rate']) else 0.0,
            'notes': notes,
            'seniorities': seniorities,
            'status': status,
            'hourly_cost': hourly_cost,
            'tags': assignment_tags.get(assignment_id, [])
        }
        assignments_dict[assignment_id] = assignment_data
    
    return assignments_dict

def get_member_tags(member_tags_df, tags_df):
    """
    Create a dictionary of member tags with numeric seniority levels
    """
    member_tags = member_tags_df.merge(
        tags_df,
        left_on='tag_id',
        right_on='id'
    )
    
    def process_group(group):
        records = group[['name']].to_dict('records')
        for record in records:
            # Use the numeric value directly
            record['seniority'] = random.choice(list(Seniority)).value  # Will be '1' to '6'
        return records
    
    return member_tags.groupby('team_member_id').apply(process_group).to_dict()

def create_consolidated_data(team_members_file, tags_file, assignments_file, 
                           assignments_tags_file, member_tags_file):
    """
    Create consolidated data structure with team members as the main entity
    """
    # Load CSV files with specified columns
    team_members_df = load_and_clean_csv(
        team_members_file,
        columns=['id', 'name', 'weekly_available_hours', 'seniority_level', 'english_level']
    )
    
    tags_df = load_and_clean_csv(
        tags_file,
        columns=['id', 'name']
    )
    
    assignments_df = load_and_clean_csv(
        assignments_file,
        columns=['id', 'client_id', 'team_member_id', 'is_team_leader', 'is_flexible', 
                'billable', 'hourly_rate', 'notes', 'seniorities', 'status', 'hourly_cost']
    )
    
    assignments_tags_df = load_and_clean_csv(assignments_tags_file)
    
    member_tags_df = load_and_clean_csv(
        member_tags_file,
        columns=['id', 'tag_id', 'team_member_id', 'seniority']
    )
    
    assignments_dict = get_assignments_with_tags(assignments_df, assignments_tags_df, tags_df)
    member_tags_dict = get_member_tags(member_tags_df, tags_df)
    
    consolidated_data = []
    for _, member in team_members_df.iterrows():
        member_id = member['id']
        
        # Handle NaN values for team member fields and convert seniority,english level to numeric
        seniority_value = '0'
        english_level_value = '0'

        if pd.notnull(member['seniority_level']):
            seniority_value = get_seniority_value(member['seniority_level'])

        if pd.notnull(member['english_level']):
            english_level_value = get_english_value(member['english_level'])

        member_data = {
            'id': member_id,
            'name': member['name'] if pd.notnull(member['name']) else "",
            'weekly_available_hours': float(member['weekly_available_hours']) if pd.notnull(member['weekly_available_hours']) else 40.0,
            'seniority_level': seniority_value,  # Now using numeric value
            'english_level': english_level_value,
            'tags': member_tags_dict.get(member_id, []),
            'assignments': []
        }
        
        # Get member's assignments
        member_assignments = assignments_df[assignments_df['team_member_id'] == member_id]
        assignments_list = [
            assignments_dict[assignment_id] 
            for assignment_id in member_assignments['id']
            if assignment_id in assignments_dict
        ]
        member_data['assignments'] = assignments_list
        
        consolidated_data.append(member_data)
    
    return consolidated_data

def main():
    files = {
        'team_members': 'team_members.csv',
        'tags': 'tags.csv',
        'assignments': 'assignments.csv',
        'assignments_tags': 'AssignmentsToTags.csv',
        'member_tags': 'tags_to_team_members.csv'
    }
    
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
  # Load tags first to get all possible tags
    tags_df = load_and_clean_csv(files['tags'], columns=['id', 'name'])
    all_tags = tags_df['name'].unique().tolist()
    
    consolidated_data = create_consolidated_data(
        files['team_members'],
        files['tags'],
        files['assignments'],
        files['assignments_tags'],
        files['member_tags']
    )
    
    json_output_path = os.path.join(output_dir, 'consolidated_team_data-2.json')
    with open(json_output_path, 'w') as f:
        json.dump(consolidated_data, f, indent=2)
    
    flattened_data = []
    for member in consolidated_data:
        base_record = {k: v for k, v in member.items() if k not in ['tags', 'assignments']}
        base_record['number_of_assignments'] = len(member['assignments'])
        base_record['active_assignments'] = sum(1 for a in member['assignments'] if a['status'] == 'active')
        base_record['importance'] = round(random.uniform(0, 100))
        base_record['tag_names'] = ', '.join([tag['name'] for tag in member['tags']])
        base_record['availability'] = round(random.uniform(21, 180))

        # Create dictionary of member's tags and their seniority levels
        # Don't convert to lowercase since we're using numbers
        member_tags_dict = {tag['name']: tag['seniority'] for tag in member['tags']}
        
        # Add column for each possible tag with seniority value or null
        for tag_name in all_tags:
            base_record[tag_name] = member_tags_dict.get(tag_name, 0)
        
        flattened_data.append(base_record)

    # Create DataFrame and arrange columns in a logical order
    df = pd.DataFrame(flattened_data)

    # Arrange columns with basic info first, then tag columns
    basic_cols = ['id', 'name', 'weekly_available_hours', 'seniority_level', 
                 'english_level', 'number_of_assignments', 'active_assignments', 'importance', 'tag_names','availability']
    tag_cols = sorted(all_tags)

   # Reorder columns
    df = df[basic_cols + tag_cols]

    # Save to CSV
    csv_output_path = os.path.join(output_dir, 'consolidated_team_data-2.csv')
    df.to_csv(csv_output_path, index=False)
    
    print("Consolidated data has been generated successfully!")
    print(f"- Full data with nested structure: {json_output_path}")
    print(f"- Simplified flat structure: {csv_output_path}")

if __name__ == "__main__":
    main()