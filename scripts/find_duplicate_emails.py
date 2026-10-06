import csv
import os
from collections import defaultdict

downloads = os.path.expanduser('~/Downloads')
applicants_file = os.path.join(downloads, 'Project Access FIN 2023 - Helsinki Bootcamp 2023 ilmoittautumiset.csv')

email_count = defaultdict(list)

with open(applicants_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        email = row.get('Mikä on sähköpostisi, {{field:25546809ff208152}}? 📨', '').strip().lower()
        first_name = row.get('Moi! Mikä on etunimesi? 👋', '').strip()
        last_name = row.get('Siistiä {{field:25546809ff208152}}, Entä sukunimesi?', '').strip()
        
        email_count[email].append(f'{first_name} {last_name}')

print('Duplicate emails:')
for email, names in email_count.items():
    if len(names) > 1:
        print(f'\n{email}:')
        for name in names:
            print(f'  - {name}')
