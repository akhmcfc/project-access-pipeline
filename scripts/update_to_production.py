with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace localhost with production URL
content = content.replace(
    'http://localhost:5000/api/2026/dashboard',
    'https://project-access-pipeline.onrender.com/api/2026/dashboard'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated index.html to use production API!')
