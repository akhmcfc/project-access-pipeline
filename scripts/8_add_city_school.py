"""
Day 8: Add city and high_school columns to candidate_mapping_2026,
populated from the merged bootcamper application data.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import sqlite3
from config.config import DATABASE_FILE, DATA_DIR

MERGED_FILE = os.path.join(DATA_DIR, 'processed', 'PA_2026_bootcampers_final.csv')

def add_city_school():
    print('')
    print('=' * 70)
    print('ADDING CITY + HIGH_SCHOOL TO candidate_mapping_2026')
    print('=' * 70)
    print('')

    df = pd.read_csv(MERGED_FILE, encoding='utf-8')

    email_col = df.columns[2]
    city_col = df.columns[5]
    school_col = df.columns[6]

    df['email_norm'] = df[email_col].astype(str).str.strip().str.lower()

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    for col_def in ['city TEXT', 'high_school TEXT']:
        col_name = col_def.split()[0]
        try:
            cursor.execute('ALTER TABLE candidate_mapping_2026 ADD COLUMN ' + col_def)
            print('Added column: ' + col_name)
        except sqlite3.OperationalError:
            print('Column already exists: ' + col_name)

    updated = 0
    not_found = []

    for _, row in df.iterrows():
        email = row['email_norm']
        city = row[city_col] if pd.notna(row[city_col]) else None
        school = row[school_col] if pd.notna(row[school_col]) else None

        cursor.execute('''
            UPDATE candidate_mapping_2026
            SET city = ?, high_school = ?
            WHERE LOWER(email) = ?
        ''', (city, school, email))

        if cursor.rowcount > 0:
            updated += 1
        else:
            not_found.append(email)

    conn.commit()

    print('')
    print('Updated: ' + str(updated) + '/' + str(len(df)))
    if not_found:
        print('WARNING: No matching candidate_id for these emails:')
        for e in not_found:
            print('   ' + e)

    cursor.execute("SELECT COUNT(*) FROM candidate_mapping_2026 WHERE city IS NOT NULL AND city != ''")
    with_city = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM candidate_mapping_2026 WHERE high_school IS NOT NULL AND high_school != ''")
    with_school = cursor.fetchone()[0]

    print('')
    print('Records with city populated: ' + str(with_city))
    print('Records with high_school populated: ' + str(with_school))

    conn.close()

    print('')
    print('=' * 70)
    print('DAY 8 COLUMN UPDATE COMPLETE')
    print('=' * 70)
    print('')

if __name__ == '__main__':
    add_city_school()
