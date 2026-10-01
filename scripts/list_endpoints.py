import sys
sys.path.insert(0, '.')
from api import create_app

app = create_app()

print('Available endpoints:')
for rule in app.url_map.iter_rules():
    if 'api' in str(rule):
        print(f'  {rule}')
