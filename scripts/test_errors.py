import requests
import json

base_url = 'http://localhost:5000/api/2026'

endpoints = [
    '/dream-universities',
    '/geographic-distribution',
    '/schools'
]

for endpoint in endpoints:
    r = requests.get(base_url + endpoint)
    data = r.json()
    print('Endpoint: ' + endpoint)
    print(json.dumps(data, indent=2))
    print()
