import sqlite3
import csv
import os
from datetime import datetime

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

# Create applications_2023 table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications_2023 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        high_school TEXT,
        city TEXT,
        dream_universities TEXT,
        field_of_study TEXT,
        target_destinations TEXT,
        was_selected BOOLEAN DEFAULT 0,
        bootcamper_id TEXT,
        submitted_at TIMESTAMP
    )
''')

# Correct filename with spaces
downloads = os.path.expanduser('~/Downloads')
applicants_file = os.path.join(downloads, 'Project Access FIN 2023 - Helsinki Bootcamp 2023 ilmoittautumiset.csv')

if not os.path.exists(applicants_file):
    print(f'ERROR: File not found!')
    exit()

print(f'Loading from: {applicants_file}')

with open(applicants_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    count = 0
    
    for row in reader:
        email = row.get('Mikä on sähköpostisi, {{field:25546809ff208152}}? 📨', '').strip().lower()
        
        if not email or email.startswith('missing'):
            continue
        
        first_name = row.get('Moi! Mikä on etunimesi? 👋', '').strip()
        last_name = row.get('Siistiä {{field:25546809ff208152}}, Entä sukunimesi?', '').strip()
        high_school = row.get('Missä olet käynyt lukion? ', '').strip()
        city = row.get('Mistä olet kotoisin? ', '').strip()
        dream_uni = row.get('Mikä on unelmayliopistosi? 🏫', '').strip()
        field = row.get('Mikä tieteenala kiinnostaa sinua eniten?📚', '').strip()
        destinations = row.get('Minne olet hakemassa?', '').strip()
        submitted = row.get('Submitted At', '').strip()
        
        try:
            cursor.execute('''
                INSERT INTO applications_2023 
                (email, first_name, last_name, high_school, city, dream_universities, field_of_study, target_destinations, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email, first_name, last_name, high_school, city, dream_uni, field, destinations, submitted))
            count += 1
        except sqlite3.IntegrityError:
            pass

conn.commit()
print(f'Loaded {count} applicants into applications_2023')
conn.close()
