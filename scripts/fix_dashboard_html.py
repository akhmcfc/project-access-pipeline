with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the key names in the dashboard
content = content.replace('data.value.fields.', 'data.value.field_distribution.')
content = content.replace('data.value.destinations.', 'data.value.destination_distribution.')
content = content.replace('const top10 = data.value.fields', 'const top10 = data.value.field_distribution')
content = content.replace('const destinations = data.value.destinations', 'const destinations = data.value.destination_distribution')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed dashboard key names!')
