"""
Configuration settings for 2026 bootcamp pipeline
"""

import os
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')

# File paths
RAW_DATA_FILE = os.path.join(DATA_DIR, 'raw', 'PA_Fin_2026_Bootcamp_Applications.csv')
DATABASE_FILE = os.path.join(DATABASE_DIR, 'project_access_2026.db')

# 2026 Configuration
BOOTCAMP_YEAR = 2026
CANDIDATE_ID_PREFIX = f"PA-{BOOTCAMP_YEAR}"

# Typeform IDs (fill in after creating forms)
SURVEY_1_FORM_ID = "INPUT_LATER"
SURVEY_2_FORM_ID = "INPUT_LATER"
SURVEY_3_FORM_ID = "INPUT_LATER"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(BASE_DIR, 'logs', f'pipeline_{datetime.now().strftime("%Y%m%d")}.log')
