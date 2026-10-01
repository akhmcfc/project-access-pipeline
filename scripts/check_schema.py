import sqlite3

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

# Get column info
cursor.execute("PRAGMA table_info(candidate_mapping_2026)")
columns = cursor.fetchall()

print('Columns in candidate_mapping_2026:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

conn.close()
