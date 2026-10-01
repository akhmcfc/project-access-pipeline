import requests
import json

r = requests.get('http://localhost:5000/api/2026/dashboard')
data = r.json()

print('dream_universities:')
print(json.dumps(data['dream_universities'][:3], indent=2))

print('\nfield_distribution:')
print(json.dumps(data['field_distribution'][:3], indent=2))
