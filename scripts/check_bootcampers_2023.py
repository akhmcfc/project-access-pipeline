import sqlite3

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM bootcampers_2023')
count = cursor.fetchone()[0]

print(f'Bootcampers in database: {count}')

if count > 0:
    cursor.execute('SELECT first_name, last_name, email FROM bootcampers_2023 LIMIT 10')
    results = cursor.fetchall()
    print('\nSample:')
    for row in results:
        print(f'  {row[0]} {row[1]} ({row[2]})')

conn.close()
