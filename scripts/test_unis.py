import requests
import json

r = requests.get('http://localhost:5000/api/2026/universities/dream')
data = r.json()
print(json.dumps(data, indent=2))
