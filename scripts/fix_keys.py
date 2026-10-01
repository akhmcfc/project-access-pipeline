import sqlite3

with open('api/models/bootcamp_queries.py', 'r') as f:
    content = f.read()

# Find and replace the get_dashboard_data return statement
old_return = '''return {
        'applicants_count': applicants_count,
        'bootcamp_count': bootcamp_count,
        'acceptance_rate': acceptance_rate,
        'dream_universities': get_dream_universities(),
        'field_distribution': get_field_distribution(),
        'destination_distribution': get_destination_distribution(),
        'geographic_distribution': get_geographic_distribution(),
        'schools': get_schools_distribution(),
        'survey_1': {'completion_rate': '100%'},
        'survey_2': {'completion_rate': '0%'},
        'survey_3': {'completion_rate': '0%'}
    }'''

new_return = '''return {
        'applicants_count': applicants_count,
        'bootcamp_count': bootcamp_count,
        'acceptance_rate': acceptance_rate,
        'dream_universities': get_dream_universities(),
        'field_distribution': get_field_distribution(),
        'destinations': get_destination_distribution(),
        'geographic_distribution': get_geographic_distribution(),
        'schools': get_schools_distribution(),
        'survey_1': get_survey_1_summary(),
        'survey_2': get_survey_2_summary(),
        'survey_3': get_survey_3_summary()
    }'''

content = content.replace(old_return, new_return)

with open('api/models/bootcamp_queries.py', 'w') as f:
    f.write(content)

print('Fixed key names!')
