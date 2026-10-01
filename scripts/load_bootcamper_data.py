import pandas as pd
import sqlite3

# Load the matched bootcampers
bootcampers_df = pd.read_csv('data/processed/2026_bootcampers_with_uni_years.csv')

# Connect to database
conn = sqlite3.connect('database/project_access_2026.db')
cursor = conn.cursor()

print('Updating candidate_mapping_2026 with university start years...')

for idx, bootcamper in bootcampers_df.iterrows():
    candidate_id = bootcamper['candidate_id']
    uni_year = int(bootcamper['uni_start_year'])
    first_name = bootcamper['first_name']
    
    # Calculate survey windows
    app_year_start = uni_year - 1
    app_year_end = uni_year
    
    survey_2_start = str(app_year_start) + '-10-01'
    survey_2_end = str(app_year_end) + '-01-31'
    survey_3_start = str(app_year_end) + '-03-01'
    survey_3_end = str(app_year_end) + '-08-31'
    
    # Add columns if they don't exist
    try:
        cursor.execute('ALTER TABLE candidate_mapping_2026 ADD COLUMN expected_uni_start_year INTEGER')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE candidate_mapping_2026 ADD COLUMN survey_2_send_start DATE')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE candidate_mapping_2026 ADD COLUMN survey_2_send_end DATE')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE candidate_mapping_2026 ADD COLUMN survey_3_send_start DATE')
    except:
        pass
    
    try:
        cursor.execute('ALTER TABLE candidate_mapping_2026 ADD COLUMN survey_3_send_end DATE')
    except:
        pass
    
    # Update the bootcamper record
    cursor.execute('''
        UPDATE candidate_mapping_2026
        SET expected_uni_start_year = ?,
            survey_2_send_start = ?,
            survey_2_send_end = ?,
            survey_3_send_start = ?,
            survey_3_send_end = ?
        WHERE candidate_id = ?
    ''', (uni_year, survey_2_start, survey_2_end, survey_3_start, survey_3_end, candidate_id))
    
    print('OK: ' + first_name)

conn.commit()
conn.close()

print('Done!')
