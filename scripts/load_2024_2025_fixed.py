import sqlite3
import csv
import os

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

downloads = os.path.expanduser('~/Downloads')

# LOAD 2024
print('Loading 2024...')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications_2024 (
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bootcampers_2024 (
        candidate_id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        city TEXT,
        high_school TEXT,
        submitted_at TIMESTAMP
    )
''')

applicants_2024_file = os.path.join(downloads, 'Project Access FIN 2024 - Helsinki Bootcamp 2024 Ilmoittautumiset.csv')
with open(applicants_2024_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
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
                INSERT INTO applications_2024 
                (email, first_name, last_name, high_school, city, dream_universities, field_of_study, target_destinations, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email, first_name, last_name, high_school, city, dream_uni, field, destinations, submitted))
        except:
            pass

# Load 2024 bootcampers
bootcamp_2024_file = os.path.join(downloads, 'Project Access FIN 2024 - Bootcamp Confirmations.csv')
bootcamp_2024_count = 0
candidate_count = 0

with open(bootcamp_2024_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get('What is your email, {{field:25546809ff208152}}? 📨', '').strip().lower()
        first_name = row.get('Hi! What was your first name again? 👋', '').strip()
        last_name = row.get('Awesome {{field:25546809ff208152}}, and your surname?', '').strip()
        participant_type = row.get('Are you a high-schooler or speaker/PA staff?', '').strip()
        bootcamp_location = row.get('To which PA Bootcamp were you confirmed to join us as a student / speaker / staff?', '').strip()
        submitted = row.get('Submitted At', '').strip()
        
        if not email or not first_name:
            continue
        if 'high' not in participant_type.lower():
            continue
        if 'Helsinki' not in bootcamp_location:
            continue
        
        candidate_id = f'PA-2024-{first_name[0:1]}{last_name[0:1]}{str(candidate_count).zfill(6)}'
        candidate_count += 1
        
        cursor.execute('SELECT city, high_school FROM applications_2024 WHERE email = ?', (email,))
        result = cursor.fetchone()
        city = result[0] if result else ''
        high_school = result[1] if result else ''
        
        try:
            cursor.execute('''
                INSERT INTO bootcampers_2024 
                (candidate_id, email, first_name, last_name, city, high_school, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (candidate_id, email, first_name, last_name, city, high_school, submitted))
            
            cursor.execute('UPDATE applications_2024 SET was_selected = 1, bootcamper_id = ? WHERE email = ?', 
                         (candidate_id, email))
            bootcamp_2024_count += 1
        except:
            pass

print(f'2024: {bootcamp_2024_count} Helsinki bootcampers')

# LOAD 2025
print('Loading 2025...')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications_2025 (
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bootcampers_2025 (
        candidate_id TEXT PRIMARY KEY,
        email TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        city TEXT,
        high_school TEXT,
        submitted_at TIMESTAMP
    )
''')

applicants_2025_file = os.path.join(downloads, 'Project Access FIN 2025 - Helsinki Bootcamp 2025 Ilmoittautumiset.csv')
with open(applicants_2025_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
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
                INSERT INTO applications_2025 
                (email, first_name, last_name, high_school, city, dream_universities, field_of_study, target_destinations, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (email, first_name, last_name, high_school, city, dream_uni, field, destinations, submitted))
        except:
            pass

# Load 2025 bootcampers (high-schoolers only - all are Helsinki)
bootcamp_2025_file = os.path.join(downloads, 'Project Access FIN 2025 - Bootcamp Confirmation.csv')
bootcamp_2025_count = 0
candidate_count = 0

with open(bootcamp_2025_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get('Email', '').strip().lower()
        first_name = row.get('First name', '').strip()
        last_name = row.get('Last name', '').strip()
        participant_type = row.get('Are you a high-schooler or speaker/PA staff?', '').strip()
        submitted = row.get('Submitted At', '').strip()
        
        if not email or not first_name:
            continue
        if 'high' not in participant_type.lower():
            continue
        
        candidate_id = f'PA-2025-{first_name[0:1]}{last_name[0:1]}{str(candidate_count).zfill(6)}'
        candidate_count += 1
        
        cursor.execute('SELECT city, high_school FROM applications_2025 WHERE email = ?', (email,))
        result = cursor.fetchone()
        city = result[0] if result else ''
        high_school = result[1] if result else ''
        
        try:
            cursor.execute('''
                INSERT INTO bootcampers_2025 
                (candidate_id, email, first_name, last_name, city, high_school, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (candidate_id, email, first_name, last_name, city, high_school, submitted))
            
            cursor.execute('UPDATE applications_2025 SET was_selected = 1, bootcamper_id = ? WHERE email = ?', 
                         (candidate_id, email))
            bootcamp_2025_count += 1
        except:
            pass

print(f'2025: {bootcamp_2025_count} Helsinki bootcampers')

conn.commit()
conn.close()
