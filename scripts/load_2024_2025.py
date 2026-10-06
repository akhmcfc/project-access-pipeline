import sqlite3
import csv
import os

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

def load_year(year, applicants_filename, bootcamp_filename):
    # Create tables
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS applications_{year} (
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
    
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS bootcampers_{year} (
            candidate_id TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            city TEXT,
            high_school TEXT,
            submitted_at TIMESTAMP
        )
    ''')
    
    downloads = os.path.expanduser('~/Downloads')
    
    # Load applicants
    applicants_file = os.path.join(downloads, applicants_filename)
    applicants_count = 0
    
    if not os.path.exists(applicants_file):
        print(f'ERROR: {applicants_file} not found')
        return
    
    with open(applicants_file, 'r', encoding='utf-8-sig') as f:
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
                cursor.execute(f'''
                    INSERT INTO applications_{year} 
                    (email, first_name, last_name, high_school, city, dream_universities, field_of_study, target_destinations, submitted_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (email, first_name, last_name, high_school, city, dream_uni, field, destinations, submitted))
                applicants_count += 1
            except sqlite3.IntegrityError:
                pass
    
    # Load bootcampers (Helsinki only)
    bootcamp_file = os.path.join(downloads, bootcamp_filename)
    bootcamp_count = 0
    candidate_count = 0
    
    if not os.path.exists(bootcamp_file):
        print(f'ERROR: {bootcamp_file} not found')
        return
    
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
            if 'high' not in participant_type.lower():
                continue
            if 'Helsinki' not in bootcamp_location:
                continue
            
            candidate_id = f'PA-{year}-{first_name[0:1]}{last_name[0:1]}{str(candidate_count).zfill(6)}'
            candidate_count += 1
            
            cursor.execute(f'SELECT city, high_school FROM applications_{year} WHERE email = ?', (email,))
            result = cursor.fetchone()
            city = result[0] if result else ''
            high_school = result[1] if result else ''
            
            try:
                cursor.execute(f'''
                    INSERT INTO bootcampers_{year} 
                    (candidate_id, email, first_name, last_name, city, high_school, submitted_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (candidate_id, email, first_name, last_name, city, high_school, submitted))
                
                cursor.execute(f'UPDATE applications_{year} SET was_selected = 1, bootcamper_id = ? WHERE email = ?', 
                             (candidate_id, email))
                bootcamp_count += 1
            except:
                pass
    
    print(f'{year}: {applicants_count} applicants, {bootcamp_count} Helsinki bootcampers')

# Load 2024 - with SPACES in filename
load_year(2024, 'Project Access FIN 2024 - Helsinki Bootcamp 2024 Ilmoittautumiset.csv', 
          'Project Access FIN 2024 - Bootcamp Confirmations.csv')

# Load 2025 - with SPACES in filename
load_year(2025, 'Project Access FIN 2025 - Helsinki Bootcamp 2025 Ilmoittautumiset.csv',
          'Project Access FIN 2025 - Bootcamp Confirmation.csv')

conn.commit()
conn.close()
