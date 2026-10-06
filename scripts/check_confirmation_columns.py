import csv
import os

downloads = os.path.expanduser('~/Downloads')
bootcamp_file = os.path.join(downloads, 'Project Access FIN 2023 - PA Bootcamp 2023 Confirmation.csv')

with open(bootcamp_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    row = next(reader)
    
    print('Column headers in confirmation file:')
    for i, col in enumerate(row.keys()):
        print(f'{i}: {col}')
