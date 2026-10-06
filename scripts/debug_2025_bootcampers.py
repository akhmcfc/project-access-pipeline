import csv
import os

downloads = os.path.expanduser('~/Downloads')
bootcamp_2025_file = os.path.join(downloads, 'Project Access FIN 2025 - Bootcamp Confirmation.csv')

high_schoolers = 0
skipped = []

with open(bootcamp_2025_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        participant_type = row.get('Are you a high-schooler or speaker/PA staff?', '').strip()
        
        if 'high' in participant_type.lower():
            high_schoolers += 1
            email = row.get('Email', '').strip().lower()
            first_name = row.get('First name', '').strip()
            
            if not email or not first_name:
                skipped.append(f'Missing email/name: {first_name} ({email})')

print(f'Total high-schoolers: {high_schoolers}')
print(f'Skipped (missing email/name): {len(skipped)}')
for s in skipped:
    print(f'  - {s}')
