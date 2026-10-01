import pandas as pd
import sqlite3

# Load all applicants
applicants_df = pd.read_csv('data/raw/PA_Fin_2026_Bootcamp_Applications.csv')
bootcampers_df = pd.read_csv('data/processed/2026_bootcampers_with_uni_years.csv')

# Normalize emails FIRST
applicants_df['Email_normalized'] = applicants_df['Email'].str.lower().str.strip()

# Drop duplicate emails (keep first)
applicants_df = applicants_df.drop_duplicates(subset=['Email_normalized'], keep='first')

print(f'Total applicants (after removing duplicates): {len(applicants_df)}')
print(f'Selected bootcampers: {len(bootcampers_df)}')

# Connect to database
conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

# Drop old table
cursor.execute('DROP TABLE IF EXISTS applications_2026')

# Create applications_2026 table
cursor.execute('''
    CREATE TABLE applications_2026 (
        id INTEGER PRIMARY KEY,
        email TEXT UNIQUE,
        first_name TEXT,
        last_name TEXT,
        high_school TEXT,
        city TEXT,
        dream_universities TEXT,
        field_of_study TEXT,
        target_destinations TEXT,
        was_selected BOOLEAN DEFAULT FALSE,
        bootcamper_id TEXT,
        submitted_at TIMESTAMP
    )
''')

print('Created applications_2026 table')

# Load all applicants
print('Loading all applicants...')
for idx, row in applicants_df.iterrows():
    email = row['Email_normalized']
    
    # Check if selected as bootcamper
    is_selected = email in bootcampers_df['email'].str.lower().str.strip().values
    bootcamper_id = None
    if is_selected:
        bootcamper_id = bootcampers_df[bootcampers_df['email'].str.lower().str.strip() == email]['candidate_id'].values[0]
    
    cursor.execute('''
        INSERT INTO applications_2026 (email, first_name, last_name, high_school, city, dream_universities, field_of_study, target_destinations, was_selected, bootcamper_id, submitted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        email,
        row.get('First name', ''),
        row.get('Last name', ''),
        row.get('Missä koulussa käyt/olet käynyt lukion? 🎓', ''),
        row.get('Missä kaupungissa asut parhaillaan? 🏠', ''),
        row.get('Mitkä yliopistot ovat toivelistallasi? (Valitse kaikki sopivat vaihtoehdot) 🏛️', ''),
        row.get('Mitä alaa aiot hakea opiskelemaan?📚', ''),
        row.get('Missä unelmoit opiskelevasi? (Valitse kaikki sopivat vaihtoehdot) 🤩', ''),
        is_selected,
        bootcamper_id,
        row.get('Submitted At', '')
    ))

conn.commit()

# Verify
cursor.execute('SELECT COUNT(*) FROM applications_2026')
total = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM applications_2026 WHERE was_selected = TRUE')
selected = cursor.fetchone()[0]

print(f'Loaded into applications_2026: {total} total, {selected} selected')
print(f'Selection rate: {(selected/total)*100:.1f}%')

conn.close()
print('Done!')
