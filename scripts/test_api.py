import requests
import json

base_url = 'http://localhost:5000/api/2026'

endpoints = [
    '/dashboard',
    '/dream-universities',
    '/fields/distribution',
    '/geographic-distribution',
    '/schools'
]

for endpoint in endpoints:
    try:
        r = requests.get(base_url + endpoint)
        data = r.json()
        print('OK: ' + endpoint)
        if 'count' in data:
            print('  Count: ' + str(data.get('count')))
        elif isinstance(data, list):
            print('  Items: ' + str(len(data)))
        else:
            print('  Keys: ' + str(list(data.keys())[:3]))
    except Exception as e:
        print('ERROR: ' + endpoint + ': ' + str(e))
    print()
