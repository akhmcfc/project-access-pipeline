import csv
import os
from collections import defaultdict

downloads = os.path.expanduser('~/Downloads')
bootcamp_2025_file = os.path.join(downloads, 'Project Access FIN 2025 - Bootcamp Confirmation.csv')

email_count = defaultdict(list)

with open(bootcamp_2025_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        participant_type = row.get('Are you a high-schooler or speaker/PA staff?', '').strip()
        
        if 'high' not in participant_type.lower():
            continue
        
        email = row.get('Email', '').strip().lower()
        first_name = row.get('First name', '').strip()
        last_name = row.get('Last name', '').strip()
        
        email_count[email].append(f'{first_name} {last_name}')

print('Duplicate emails (2025 high-schoolers):')
for email, names in email_count.items():
    if len(names) > 1:
        print(f'\n{email}:')
        for name in names:
            print(f'  - {name}')
