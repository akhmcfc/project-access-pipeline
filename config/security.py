"""
SECURITY CONFIGURATION
"""

import os
from functools import wraps

PRIVATE_TABLES = {
    'candidate_mapping_2026': {
        'description': 'Email-to-ID mapping - NEVER expose',
        'fields': ['email', 'first_name', 'last_name', 'candidate_id'],
        'access': 'ADMIN_ONLY'
    }
}

PUBLIC_TABLES = {
    'pre_bootcamp_2026': {
        'description': 'Survey 1 data - Anonymous',
        'fields': ['candidate_id', 'dream_universities', 'target_destinations', 'field_of_study', 'confidence_level'],
        'access': 'PUBLIC'
    },
    'mid_bootcamp_2026': {
        'description': 'Survey 2 data - Anonymous',
        'fields': ['candidate_id', 'changed_universities', 'changed_destination', 'updated_confidence_level'],
        'access': 'PUBLIC'
    },
    'post_bootcamp_2026': {
        'description': 'Survey 3 data - Anonymous',
        'fields': ['candidate_id', 'universities_applied_to', 'final_destination_choice', 'bootcamp_impact_final'],
        'access': 'PUBLIC'
    }
}

ADMIN_PASSWORD = os.getenv('PA_ADMIN_PASSWORD', 'CHANGE_ME_NOW')

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify
        password = request.headers.get('X-Admin-Password')
        if password != ADMIN_PASSWORD:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def log_data_access(action, table, user, success):
    import os
    os.makedirs('logs', exist_ok=True)
    with open('logs/security_audit.log', 'a') as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        status = "SUCCESS" if success else "FAILED"
        f.write(f"{timestamp} | {action} | {table} | {user} | {status}\n")
