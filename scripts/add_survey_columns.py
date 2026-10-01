import sqlite3

conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

# Add missing columns
try:
    cursor.execute('ALTER TABLE candidate_mapping_2026 ADD COLUMN survey_2_sent_date DATE')
    print('Added survey_2_sent_date')
except:
    print('survey_2_sent_date already exists')

try:
    cursor.execute('ALTER TABLE candidate_mapping_2026 ADD COLUMN survey_3_sent_date DATE')
    print('Added survey_3_sent_date')
except:
    print('survey_3_sent_date already exists')

conn.commit()
conn.close()
print('Done!')
