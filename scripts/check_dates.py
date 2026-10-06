import sqlite3

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

# Check what's in the database
cursor.execute('SELECT candidate_id, first_name, survey_2_send_start, survey_2_send_end, survey_2_sent_date FROM candidate_mapping_2026 LIMIT 5')
results = cursor.fetchall()

print('Sample data from database:')
for row in results:
    print(row)

conn.close()
