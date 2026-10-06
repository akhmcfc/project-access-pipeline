import sqlite3
import csv
import os

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS outcomes_all_years (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bootcamper_id TEXT,
        year INTEGER,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        applied_abroad TEXT,
        universities_applied_abroad TEXT,
        received_offer_abroad TEXT,
        offers_from_universities TEXT,
        studying_abroad TEXT,
        university_abroad TEXT,
        field_abroad TEXT,
        reason_not_abroad TEXT,
        applied_finland TEXT,
        university_finland TEXT,
        field_finland TEXT,
        future_plans TEXT,
        consent_resend TEXT,
        submitted_at TIMESTAMP
    )
''')

downloads = os.path.expanduser('~/Downloads')
outcomes_file = os.path.join(downloads, 'PAF Data tracking - Ex-Bootcamper Survey spring 2026 _ Survey 3.csv')

if not os.path.exists(outcomes_file):
    print(f'ERROR: {outcomes_file}')
    exit()

loaded = 0

with open(outcomes_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        email = row.get('Email', '').strip().lower()
        if not email:
            continue
        
        year = row.get('Which year did you attend the bootcamp? 🕺', '').strip()
        first_name = row.get('First name', '').strip()
        last_name = row.get('Last name', '').strip()
        
        bootcamper_id = None
        # Only search 2023-2025 (2026 bootcampers not selected yet)
        for y in [2023, 2024, 2025]:
            cursor.execute(f'SELECT candidate_id FROM bootcampers_{y} WHERE email = ?', (email,))
            result = cursor.fetchone()
            if result:
                bootcamper_id = result[0]
                break
        
        applied_abroad = row.get('Have you applied to any *university outside *Finland?', '').strip()
        universities_applied = row.get('Which universities did you apply to?', '').strip()
        received_offer = row.get('Did you receive an offer from any university abroad?', '').strip()
        offers_from = row.get('Congratulations! From *{{field:q4_where_applied}}*, which ones did you receive offers from?', '').strip()
        studying_abroad = row.get('Are you currently studying at a university abroad?', '').strip()
        uni_abroad = row.get('Which university abroad are you studying at, out of the ones you got offers from (*{{field:q6_offer_unis}}*)?', '').strip()
        field_abroad = row.get('*Optional:* What are you studying?', '').strip()
        reason_not_abroad = row.get('What influenced your decision not to study abroad?', '').strip()
        applied_finland = row.get('Have you applied to a university in Finland?', '').strip()
        uni_finland = row.get('Which university in Finland are you studying at (or have you been accepted to)?', '').strip()
        field_finland = row.get('Optional: What are you studying?', '').strip()
        future_plans = row.get('Which universities are you planning on applying to?', '').strip()
        consent = row.get('Could we send this survey to you again once  you\'ve applied/received your results?', '').strip()
        submitted = row.get('Submitted At', '').strip()
        
        try:
            cursor.execute('''
                INSERT INTO outcomes_all_years 
                (bootcamper_id, year, first_name, last_name, email, applied_abroad, universities_applied_abroad, received_offer_abroad, offers_from_universities, studying_abroad, university_abroad, field_abroad, reason_not_abroad, applied_finland, university_finland, field_finland, future_plans, consent_resend, submitted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (bootcamper_id, year, first_name, last_name, email, applied_abroad, universities_applied, received_offer, offers_from, studying_abroad, uni_abroad, field_abroad, reason_not_abroad, applied_finland, uni_finland, field_finland, future_plans, consent, submitted))
            loaded += 1
        except:
            pass

conn.commit()
print(f'Loaded {loaded} outcome records')
conn.close()
