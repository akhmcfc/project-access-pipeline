import sqlite3
import csv
import os
from datetime import datetime

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

# Create bootcampers_2023 table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bootcampers_2023 (
        candidate_id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        city TEXT,
        high_school TEXT,
        submitted_at TIMESTAMP
    )
''')

# Find bootcampers confirmation file
possible_paths = [
    'Project_Access_FIN_2023_-_PA_Bootcamp_2023_Confirmation.csv',
    'data/raw/Project_Access_FIN_2023_-_PA_Bootcamp_2023_Confirmation.csv',
    os.path.expanduser('~/Downloads/Project_Access_FIN_2023_-_PA_Bootcamp_2023_Confirmation.csv'),
    '/mnt/user-data/uploads/Project_Access_FIN_2023_-_PA_Bootcamp_2023_Confirmation.csv'
]

bootcamp_file = None
for path in possible_paths:
    if os.path.exists(path):
        bootcamp_file = path
        print(f'Found file at: {bootcamp_file}')
        break

if not bootcamp_file:
    print('ERROR: Could not find bootcamp confirmation file!')
    print('Checked:')
    for p in possible_paths:
        print(f'  - {p}')
    exit()

# Generate candidate IDs
candidate_count = 0

with open(bootcamp_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        email = row.get('What is your email, {{field:25546809ff208152}}? 📨', '').strip().lower()
        
        if not email or email.startswith('missing'):
            continue
        
        # Filter: only bootcampers (not speakers/staff)
        participant_type = row.get('Are you a high-schooler or speaker/PA staff?', '').strip()
        
        # Only include actual bootcamp students
        if 'Speaker' in participant_type or 'staff' in participant_type.lower():
            continue
        
        first_name = row.get('Hi! What was again your first name? 👋', '').strip()
        last_name = row.get('Awesome {{field:25546809ff208152}}, and your surname?', '').strip()
        submitted = row.get('Submitted At', '').strip()
        
        # Generate candidate ID
        candidate_id = f'PA-2023-{first_name[0:1]}{last_name[0:1]}{str(candidate_count).zfill(6)}'
        candidate_count += 1
        
        # Get city from applicants table if exists
        cursor.execute('SELECT city, high_school FROM applications_2023 WHERE email = ?', (email,))
        result = cursor.fetchone()
        city = result[0] if result else ''
        high_school = result[1] if result else ''
        
        try:
            cursor.execute('''
                INSERT INTO bootcampers_2023 
                (candidate_id, email, first_name, last_name, city, high_school, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (candidate_id, email, first_name, last_name, city, high_school, submitted))
            
            # Mark as selected in applications table
            cursor.execute('UPDATE applications_2023 SET was_selected = 1, bootcamper_id = ? WHERE email = ?', 
                         (candidate_id, email))
        except Exception as e:
            print(f'  Error for {first_name}: {e}')

conn.commit()

# Count results
cursor.execute('SELECT COUNT(*) FROM bootcampers_2023')
bootcamp_count = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM applications_2023 WHERE was_selected = 1')
selected_count = cursor.fetchone()[0]

print(f'Loaded {bootcamp_count} bootcampers into bootcampers_2023')
print(f'Marked {selected_count} as selected in applications_2023')

conn.close()
