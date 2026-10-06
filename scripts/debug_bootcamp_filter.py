import csv
import os

downloads = os.path.expanduser('~/Downloads')
bootcamp_file = os.path.join(downloads, 'Project Access FIN 2023 - PA Bootcamp 2023 Confirmation.csv')

with open(bootcamp_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    high_schoolers = 0
    staff = 0
    other = 0
    
    for row in reader:
        participant_type = row.get('Are you a high-schooler or speaker/PA staff?', '').strip()
        first_name = row.get('Hi! What was again your first name? 👋', '').strip()
        
        if 'Speaker' in participant_type or 'staff' in participant_type.lower():
            staff += 1
        elif 'high' in participant_type.lower():
            high_schoolers += 1
        else:
            other += 1
            if other <= 5:
                print(f'Unknown type for {first_name}: {participant_type}')

print(f'\nTotal: {high_schoolers + staff + other}')
print(f'High-schoolers: {high_schoolers}')
print(f'Staff/Speakers: {staff}')
print(f'Other/Unknown: {other}')
