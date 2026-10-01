import sqlite3

# Read bootcamp_queries.py
with open('api/models/bootcamp_queries.py', 'r') as f:
    content = f.read()

# Find and replace the get_dashboard_data function
old_func = '''def get_dashboard_data():
    """Get all dashboard data"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Count applicants and bootcampers
    cursor.execute('SELECT COUNT(*) FROM applications_2026')
    applicants_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM candidate_mapping_2026')
    bootcamp_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Calculate acceptance rate (placeholder)
    acceptance_rate = 'TBD'
    
    return {
        'applicants_count': applicants_count,
        'bootcamp_count': bootcamp_count,
        'acceptance_rate': acceptance_rate
    }'''

new_func = '''def get_dashboard_data():
    """Get all dashboard data"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Count applicants and bootcampers
    cursor.execute('SELECT COUNT(*) FROM applications_2026')
    applicants_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM candidate_mapping_2026')
    bootcamp_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Calculate acceptance rate (placeholder)
    acceptance_rate = 'TBD'
    
    return {
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

content = content.replace(old_func, new_func)

with open('api/models/bootcamp_queries.py', 'w') as f:
    f.write(content)

print('Updated get_dashboard_data()')
