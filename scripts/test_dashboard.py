import requests
import json

r = requests.get('http://localhost:5000/api/2026/dashboard')
data = r.json()

print('Dashboard data keys:')
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in data.items()}, indent=2))
