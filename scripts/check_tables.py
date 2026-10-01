import sqlite3
conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=?', ('table',))
tables = cursor.fetchall()
print('Tables in database:')
for table in tables:
    print(f'  - {table[0]}')
    cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
    count = cursor.fetchone()[0]
    print(f'    Rows: {count}')
conn.close()
