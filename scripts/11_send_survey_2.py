import pandas as pd
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys

# Add config path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DATABASE_FILE, TYPEFORM_API_TOKEN

# Load personalized links
links_df = pd.read_csv('data/processed/2026_personalized_links.csv')

# Connect to database
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

print('Checking for bootcampers ready for Survey 2...\n')

today = datetime.now().date()
survey_2_sent = []
already_sent = []
not_ready = []

for idx, row in links_df.iterrows():
    candidate_id = row['candidate_id']
    email = row['email'].lower().strip()
    first_name = row['first_name']
    survey_2_link = row['survey2_link']
    
    # Get survey send window from database
    cursor.execute('''
        SELECT survey_2_send_start, survey_2_send_end, survey_2_sent_date
        FROM candidate_mapping_2026
        WHERE candidate_id = ?
    ''', (candidate_id,))
    
    result = cursor.fetchone()
    
    if not result:
        print(f'  WARNING: {first_name} not found in database')
        continue
    
    send_start_str, send_end_str, sent_date = result
    
    # Parse dates
    try:
        send_start = datetime.strptime(send_start_str, '%Y-%m-%d').date()
        send_end = datetime.strptime(send_end_str, '%Y-%m-%d').date()
    except:
        print(f'  ERROR parsing dates for {first_name}')
        continue
    
    # Check if already sent
    if sent_date:
        already_sent.append(first_name)
        continue
    
    # Check if within send window
    if send_start <= today <= send_end:
        print(f'  READY: {first_name} ({email})')
        print(f'    Send window: {send_start} to {send_end}')
        print(f'    Link: {survey_2_link}')
        survey_2_sent.append((candidate_id, first_name, email, survey_2_link))
    else:
        not_ready.append((first_name, send_start, send_end))

print(f'\n=== SUMMARY ===')
print(f'Ready to send: {len(survey_2_sent)}')
print(f'Already sent: {len(already_sent)}')
print(f'Not yet ready: {len(not_ready)}')

if not_ready:
    print(f'\nNot yet ready (coming up):')
    for name, start, end in not_ready[:5]:
        print(f'  - {name}: {start} to {end}')

# If there are bootcampers ready, mark them as sent
if survey_2_sent:
    print(f'\nMarking {len(survey_2_sent)} as sent in database...')
    for candidate_id, first_name, email, link in survey_2_sent:
        cursor.execute('''
            UPDATE candidate_mapping_2026
            SET survey_2_sent_date = ?
            WHERE candidate_id = ?
        ''', (today, candidate_id))
        print(f'  Marked: {first_name}')
    
    conn.commit()
    print('Done!')

conn.close()

print('\nNote: Email sending not yet implemented.')
print('Survey 2 ready list:')
for candidate_id, first_name, email, link in survey_2_sent:
    print(f'  {email}: {link}')
