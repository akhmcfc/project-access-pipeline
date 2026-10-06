import sqlite3
import csv
import os

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM bootcampers_2023')  # Clear previous failed attempt

downloads = os.path.expanduser('~/Downloads')
bootcamp_file = os.path.join(downloads, 'Project Access FIN 2023 - PA Bootcamp 2023 Confirmation.csv')

candidate_count = 0
loaded = 0

with open(bootcamp_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        email = row.get('What is your email, {{field:25546809ff208152}}? 📨', '').strip().lower()
        first_name = row.get('Hi! What was again your first name? 👋', '').strip()
        last_name = row.get('Awesome {{field:25546809ff208152}}, and your surname?', '').strip()
        participant_type = row.get('Are you a high-schooler or speaker/PA staff?', '').strip()
        submitted = row.get('Submitted At', '').strip()
        
        if not email or not first_name:
            continue
        
        # Only load high-schoolers
        if 'high' not in participant_type.lower():
            continue
        
        candidate_id = f'PA-2023-{first_name[0:1]}{last_name[0:1]}{str(candidate_count).zfill(6)}'
        candidate_count += 1
        
        # Get from applicants
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
            
            cursor.execute('UPDATE applications_2023 SET was_selected = 1, bootcamper_id = ? WHERE email = ?', 
                         (candidate_id, email))
            loaded += 1
        except Exception as e:
            print(f'Error: {e}')

conn.commit()
print(f'Loaded {loaded} bootcampers')
conn.close()
