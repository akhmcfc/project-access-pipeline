import csv
import os

downloads = os.path.expanduser('~/Downloads')

for year in [2024, 2025]:
    if year == 2024:
        filename = 'Project Access FIN 2024 - Bootcamp Confirmations.csv'
    else:
        filename = 'Project Access FIN 2025 - Bootcamp Confirmation.csv'
    
    filepath = os.path.join(downloads, filename)
    
    print(f'\n{year} Column headers:')
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, col in enumerate(reader.fieldnames[:13]):
            print(f'{i}: {col}')
