import sqlite3
import csv
import os

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

# Clear 2023 bootcampers and reload with Helsinki filter
cursor.execute('DELETE FROM bootcampers_2023')

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
        bootcamp_location = row.get('To which PA Bootcamp were you confirmed to join us as a student / speaker / staff?', '').strip()
        submitted = row.get('Submitted At', '').strip()
        
        if not email or not first_name:
            continue
        
        # Filter: high-schoolers only
        if 'high' not in participant_type.lower():
            continue
        
        # Filter: Helsinki bootcamp only
        if 'Helsinki' not in bootcamp_location:
            continue
        
        candidate_id = f'PA-2023-{first_name[0:1]}{last_name[0:1]}{str(candidate_count).zfill(6)}'
        candidate_count += 1
        
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
            loaded += 1
        except:
            pass

conn.commit()
print(f'2023 Helsinki bootcampers: {loaded}')
conn.close()
