import sqlite3

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

# Clear the test data - mark all as NOT sent
cursor.execute('UPDATE candidate_mapping_2026 SET survey_2_sent_date = NULL')

conn.commit()
conn.close()

print('Cleared test data - all ready to send')
