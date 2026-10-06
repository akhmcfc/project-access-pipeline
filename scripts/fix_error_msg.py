with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update error message
content = content.replace(
    'Error loading dashboard. Make sure API is running on localhost:5000',
    'Error loading dashboard. Check network connection and API status.'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated error message!')
