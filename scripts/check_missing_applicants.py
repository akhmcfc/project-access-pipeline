import csv
import os

downloads = os.path.expanduser('~/Downloads')
applicants_file = os.path.join(downloads, 'Project Access FIN 2023 - Helsinki Bootcamp 2023 ilmoittautumiset.csv')

with open(applicants_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    total = 0
    with_email = 0
    no_email = []
    
    for row in reader:
        total += 1
        email = row.get('Mikä on sähköpostisi, {{field:25546809ff208152}}? 📨', '').strip().lower()
        first_name = row.get('Moi! Mikä on etunimesi? 👋', '').strip()
        last_name = row.get('Siistiä {{field:25546809ff208152}}, Entä sukunimesi?', '').strip()
        
        if email and not email.startswith('missing'):
            with_email += 1
        else:
            no_email.append(f'{first_name} {last_name}')

print(f'Total rows: {total}')
print(f'With email: {with_email}')
print(f'Missing email: {len(no_email)}')
print(f'\nMissing email:')
for name in no_email:
    print(f'  - {name}')
